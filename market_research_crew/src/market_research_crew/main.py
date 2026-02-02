import warnings
from market_research_crew.crew import MarketResearchCrew
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        "product_idea": "An AI powered tool that summarizes youtube videos on my channel and posts the summary on various social media platforms like LinkedIn, Instagram, Facebook,X, WhatsApp"
    }

    try:
        # Pre-flight LLM check: provide actionable guidance if no backend is available
        try:
            from crewai.utilities.llm_utils import create_llm

            # This will raise an exception if no provider is configured and LiteLLM isn't installed
            create_llm()
        except Exception as llm_err:
            raise RuntimeError(
                "No LLM backend available. Please either set up a native provider (e.g., set OPENAI_API_KEY) "
                "or install LiteLLM locally (run: pip install litellm). Original error: "
                f"{llm_err}"
            ) from llm_err

        MarketResearchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()