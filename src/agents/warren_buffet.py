# src/agents/warren_buffet.py
from ..graph.state import AgentState, AgentSignal
from ..tools.api import get_price_history, get_latest_price
from ..llm.llmservice import get_openai_service
import json

def analyze(state: AgentState) -> AgentState:
    """Warren Buffett Agent — looks for stability and fair price."""
    try:
        ticker = state.ticker
        hist = get_price_history(ticker, period="6mo")

        if hist is None or hist.empty:
            state.agent_signal = AgentSignal(action="hold", confidence=0.5)
            state.signals["Buffett"] = {"action": "hold", "confidence": 0.5}
            state.reasoning["Buffett"] = f"No price history found for {ticker}, default HOLD."
            return state

        # Calculate volatility
        pct_changes = hist["Close"].pct_change()
        volatility = pct_changes.std() * 100  # % volatility
        
        # Print for debugging
        print(f"DEBUG: {ticker} volatility = {volatility:.2f}%")

        # Traditional analysis
        if volatility < 2:  # very stable
            action, conf = "buy", 0.8
        elif volatility < 5:  # moderate
            action, conf = "hold", 0.6
        else:  # too volatile
            action, conf = "sell", 0.7

        # Get LLM analysis
        llm_analysis = None
        try:
            llm_analysis = get_llm_analysis(state, ticker, volatility)
        except Exception as e:
            print(f"DEBUG: LLM service not available: {e}")
            state.reasoning["Buffett_LLM"] = f"LLM service not available: {e}"
        
        # Print LLM reasoning for debugging
        if llm_analysis:
            print(f"DEBUG: LLM Analysis for {ticker} = {llm_analysis}")
        
        # Combine traditional analysis with LLM insights
        if llm_analysis:
            # If LLM analysis is available, blend it with our analysis
            llm_confidence = llm_analysis.get("confidence", 0.5)
            llm_action = llm_analysis.get("action", "hold")
            
            # Weight our analysis more heavily (70%) but incorporate LLM insights (30%)
            blended_confidence = (conf * 0.7) + (llm_confidence * 0.3)
            conf = blended_confidence
            
            # Add LLM reasoning to our reasoning
            llm_reasoning = llm_analysis.get("reasoning", "")
            state.reasoning["Buffett_LLM"] = llm_reasoning

        state.agent_signal = AgentSignal(action=action, confidence=conf)
        state.signals["Buffett"] = {"action": action, "confidence": conf}
        state.reasoning["Buffett"] = (
            f"Volatility = {volatility:.2f}%. Interpreted as {action.upper()} ({conf*100:.0f}%)."
        )

    except Exception as e:
        state.agent_signal = AgentSignal(action="hold", confidence=0.5)
        state.signals["Buffett"] = {"action": "hold", "confidence": 0.5}
        state.reasoning["Buffett"] = f"Error during Buffett analysis: {e}"

    return state

def get_llm_analysis(state: AgentState, ticker: str, volatility: float) -> dict:
    """
    Get Analysis from LLM Service
    Args:
        state (AgentState): Agent State
        ticker (str): Ticker Symbol
        volatility (float): Volatility
    Returns:
        Dictionary with LLM analysis or empty dict if error
    """
    # List of OpenRouter free models to try in order of preference
    models = [
        "meta-llama/llama-3.1-8b-instruct",  # Free Meta model
    ]
    
    try:
        #Initialize LLM Service
        llm_service = get_openai_service()

        #Creating a Prompt from LLM Analysis
        prompt = f"""
        As Warren Buffett, analyze this investment opportunity:
        
        Ticker: {ticker}
        Current Volatility: {volatility:.2f}%
        Portfolio Value: ${state.portfolio_value:.2f}
        Cash Available: ${state.cash:.2f}
        Current Holdings: {state.holdings} shares
        
        Based on your value investing principles, provide:
        1. Whether to buy, sell, or hold
        2. Confidence level (0.0 to 1.0)
        3. Brief reasoning (1-2 sentences)
        
        Respond in JSON format:
        {{
            "action": "buy|sell|hold",
            "confidence": 0.0-1.0,
            "reasoning": "brief explanation"
        }}
        """
        
        print(f"DEBUG: Sending prompt to LLM for {ticker}")
        print(f"DEBUG: Prompt length: {len(prompt)} characters")
        
        # Try different models until one works
        for model in models:
            try:
                print(f"DEBUG: Trying model {model}")
                # Get completion from LLM
                response_text = llm_service.get_completion(
                    model=model,
                    prompt=prompt,
                    temperature=0.5,  # Moderate temperature for balanced responses
                    max_tokens=200  # Limit response length to reduce rate limiting
                )
                
                print(f"DEBUG: Received response from {model}: {response_text[:100]}...")
                
                # Try to parse JSON response
                try:
                    result = json.loads(response_text)
                    print(f"DEBUG: Successfully parsed JSON from {model}")
                    return result
                except json.JSONDecodeError:
                    # If JSON parsing fails, continue to next model
                    print(f"DEBUG: Failed to parse JSON response from {model}")
                    continue
                    
            except Exception as e:
                print(f"DEBUG: Failed to get response from {model}: {e}")
                continue
        
        # If all models fail, return basic analysis
        print("DEBUG: All models failed, returning default response")
        return {
            "action": "hold",
            "confidence": 0.5,
            "reasoning": "Unable to get LLM response from any available models"
        }
            
    except Exception as e:
        # Return empty dict if LLM analysis fails
        print(f"LLM analysis failed: {e}")
        return {}