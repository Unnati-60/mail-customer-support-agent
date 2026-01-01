import asyncio

import opik
import logging
import json
from opik.evaluation import evaluate
from opik.evaluation.models import OpikBaseModel
from opik.evaluation.metrics import BaseMetric, score_result
from opik.evaluation.metrics import AnswerRelevance 
from src.application.workflow.chains import build_chain
from src.prompt import SQL_EVALUATION_PROMPT
from src.config import settings
from src.application.generate_response import get_response
from src.application.workflow.state import AgentState, state_to_str
from opik.evaluation.models import OpikBaseModel
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from typing import Any
from src.utils import normalize_db_output


class SQLAccuracyMetric(BaseMetric):
    """
    LLM-as-Judge metric for evaluating SQL query accuracy.
    """
    def __init__(self, name: str = "Sql accuracy metric",model: str = settings.GROQ_LLM_MODEL):
        super().__init__(name=name)
        self.model = model
    
    def score(
        self, 
        customer_query: str,
        expected_sql,
        generated_sql,
        expected_sql_output: list[any], 
        generated_sql_output: list[any],
        **kwargs) -> dict:

        try:
            chain = build_chain(system_prompt=SQL_EVALUATION_PROMPT)
            raw= generated_sql_output.to_dict(orient="records")
            generated_sql_output= normalize_db_output(raw)

            input_vars = {
                "user_query": customer_query,
                "expected_sql": expected_sql,
                "generated_sql": generated_sql,
                "expected_sql_output": expected_sql_output,
                "generated_sql_output": generated_sql_output
            }

            response = chain.invoke(
                input_vars
            )
            evaluation = json.loads(response.content.strip().removeprefix("```json").removesuffix("```").strip())

            return score_result.ScoreResult(
                    name=self.name,
                    value=float(evaluation.get("score")),
                    reason=evaluation.get("reasoning")
                )
        except Exception as e:
            logging.error(f"Error in LLM evaluation: {e}")
            return score_result.ScoreResult(
                    name=SQLAccuracyMetric.__name__,
                    value=0.0,
                    reason=f"Error in LLM evaluation: {e}"
                )
    
    
class QueryClassificationMetric(BaseMetric):
    """
    Checks if the agent correctly classified the query type
    """
    def __init__(self, name: str = "query_classification_accuracy"):
        super().__init__(name=name)
    
    def score(
        self,
        expected_query_type: str,
        generated_query_type: str,
        **kwargs
    ) -> float:
        """
        Compare query type classification
        """
        if expected_query_type == generated_query_type:
            return score_result.ScoreResult(
                name=QueryClassificationMetric.__name__,
                value=1.0,
                reason=f"Correctly classified as '{expected_query_type}'"
            )
        return score_result.ScoreResult(
            name=QueryClassificationMetric.__name__,
            value=0.0,
            reason=f"Expected '{expected_query_type}' but got '{generated_query_type}'"
        )
    
class ChatGroqOpikModel(OpikBaseModel):
    def __init__(self):
        super().__init__(settings.GROQ_LLM_MODEL)
        self.chat_model = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_LLM_MODEL
        )

    def generate_string(self, input: str, **kwargs: Any) -> str:
        try:
            response = self.chat_model.invoke(input)
            return response.content or ""
        except Exception as e:
            raise RuntimeError(f"Groq judge failed: {e}")

    def generate_provider_response(
        self, messages: list[dict[str, Any]], **kwargs: Any
    ) -> Any:
        # Convert Opik-style messages → LangChain messages
        lc_messages = [
            HumanMessage(content=m["content"])
            for m in messages
            if m["role"] == "user"
        ]

        response = self.chat_model.invoke(lc_messages)

        # Return OpenAI-like structure (what Opik expects internally)
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response.content,
                    }
                }
            ]
        }


async def evaluation_task(x: dict) -> dict:
    """Calls agentic app logic to evaluate philosopher responses.

    Args:
        x: Dictionary containing evaluation data with the following keys:
            

    Returns:
        dict: Dictionary with evaluation results.  

    """

    input_mail = x["customer_mail"]

    result, latest_state = await get_response(
        customer_email=input_mail
    )
    
    # latest_state = state_to_str(latest_state)



    return {
        "input": input_mail,
        "output": result,  
        "customer_email": x["customer_mail"],
        "expected_sql": x["expected_sql"],
        "expected_sql_output": x["expected_sql_output"],
        "expected_query_type": x["query_type"],
        "labels": x.get("labels", []),
        "customer_query": latest_state["customer_query"],
        "response_email": latest_state["response_email"],
        "generated_query_type": latest_state["query_type"],
        "generated_sql": latest_state["sql_query_v2"],
        "generated_sql_output": latest_state["sql_output_v2"],
        "context": x["expected_sql_output"]
        
    }


def get_used_prompts() -> list[opik.Prompt]:
    client = opik.Opik()

    prompts = [
        client.get_prompt(name="extract_classify_query_prompt"),
        client.get_prompt(name="sql_prompt"),
        client.get_prompt(name="reflect_sql_prompt"),
        client.get_prompt(name="email_prompt")
    ]
    prompts = [p for p in prompts if p is not None]

    return prompts


def evaluate_agent(
    dataset: opik.Dataset | None,
    workers: int = 2,
    nb_samples: int | None = None,
) -> None:
    """Evaluates an agent using specified metrics and dataset.

    Runs evaluation using Opik framework with configured metrics for
    answer relevance, query classification, SQL accuracy, and email response quality.

    Args:
        dataset: Dataset containing evaluation examples.
        workers: Number of parallel workers to use for evaluation.
            Defaults to 2.
        nb_samples: Optional number of samples to evaluate.
            If None, evaluates the entire dataset.

    Raises:
        ValueError: If dataset is None
        AssertionError: If COMET_API_KEY is not set

    Returns:
        None
    """

    assert settings.COMET_API_KEY, (
        "COMET_API_KEY is not set. We need it to track the experiment with Opik."
    )

    if not dataset:
        raise ValueError("Dataset is 'None'.")

    logging.info("Starting evaluation...")

    experiment_config = {
        "model_id": settings.GROQ_LLM_MODEL,
        "dataset_name": dataset.name,
    }

    used_prompts = get_used_prompts()

    scoring_metrics = [
        QueryClassificationMetric(),
        SQLAccuracyMetric(),
        AnswerRelevance(model=ChatGroqOpikModel())
    ]

    logging.info("Evaluation details:")
    logging.info(f"Dataset: {dataset.name}")
    logging.info(f"Metrics: {[m.__class__.__name__ for m in scoring_metrics]}")

    evaluate(
        dataset=dataset,
        task=lambda x: asyncio.run(evaluation_task(x)),
        scoring_metrics=scoring_metrics,
        experiment_config=experiment_config,
        task_threads=workers,
        nb_samples=nb_samples,
        prompts=used_prompts,
    )


