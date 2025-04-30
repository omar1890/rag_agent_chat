from langchain.callbacks.base import BaseCallbackHandler

class ToolLoggerCallbackHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "UnknownTool")
        print(f"Tool used: {tool_name}")
        print(f"Input: {input_str}")

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM called with prompt: {prompts[0]}")

    def on_llm_end(self, response, **kwargs):
        usage = response.llm_output.get("token_usage", {})
        print(f"LLM token usage: {usage}")