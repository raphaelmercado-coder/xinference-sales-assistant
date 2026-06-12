# Xinference: The OpenAI-Compatible API

Once a model is running, Xinference can be used through a web UI, the command line,
cURL, the Xinference Python client, or its REST API.

The REST API is compatible with the OpenAI API. This means existing code written for
the OpenAI SDK works against Xinference by changing only the base URL to point at the
Xinference endpoint plus the /v1 path. The API key field is still required by the SDK
but is not used for authentication by a default local server.

Because of this compatibility, switching the underlying model or provider is a
configuration change rather than an application rewrite. The same client code can call
GPT one day and a self-hosted open model the next.

Xinference also integrates with popular third-party libraries including LangChain,
LlamaIndex, Dify, and Chatbox, so it slots into existing application frameworks
without custom glue code.
