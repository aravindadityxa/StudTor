import os
import httpx
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LocalLLMClient:
    """Ollama local LLM client for offline AI responses."""

    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
        self.timeout = 300  # 5 minute timeout for long responses
        print(f"DEBUG: LocalLLMClient initialized")
        print(f"DEBUG: Ollama URL: {self.ollama_url}")
        print(f"DEBUG: Model: {self.model}")

    def is_ollama_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            with httpx.Client(timeout=5) as client:
                response = client.get(f"{self.ollama_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            print(f"DEBUG: Ollama connection error: {e}")
            return False

    def is_model_available(self) -> bool:
        """Check if the required model is available."""
        try:
            with httpx.Client(timeout=5) as client:
                response = client.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    models = [m["name"].split(":")[0] for m in data.get("models", [])]
                    return self.model.split(":")[0] in models
        except Exception as e:
            print(f"DEBUG: Model check error: {e}")
        return False

    def get_status(self) -> dict:
        """Get Ollama and model status."""
        return {
            "ollama_running": self.is_ollama_running(),
            "model_available": self.is_model_available(),
            "model": self.model,
            "ollama_url": self.ollama_url,
        }

    def generate_response(self, message: str, language: str = "en") -> str:
        """Generate response from local LLM using Ollama."""
        try:
            if not self.is_ollama_running():
                return self._get_fallback_response(
                    "Ollama is not running. Please start Ollama to use this feature.",
                    language,
                )

            if not self.is_model_available():
                return self._get_fallback_response(
                    f"Model {self.model} is not available. Please run setup_ollama.bat to download it.",
                    language,
                )

            system_prompt = self._get_system_prompt(language)
            full_prompt = f"{system_prompt}\n\nUser: {message}\n\nProvide a helpful learning response with:\n- Clear explanation\n- Key points\n- Practical examples\n\nAssistant:"

            print(f"DEBUG: Sending request to Ollama for model: {self.model}")

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False,
                        "temperature": 0.7,
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    result = data.get("response", "").strip()
                    if result:
                        print(f"DEBUG: ✅ Response generated successfully")
                        return result
                    else:
                        print(f"DEBUG: Empty response from Ollama")
                        return self._get_fallback_response(
                            "No response generated. Please try again.",
                            language,
                        )
                else:
                    error_msg = f"Ollama error: {response.status_code}"
                    print(f"DEBUG: {error_msg}")
                    return self._get_fallback_response(error_msg, language)

        except httpx.TimeoutException:
            msg = "Request timed out. The model is taking too long to respond."
            print(f"DEBUG: Timeout error: {msg}")
            return self._get_fallback_response(msg, language)
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"DEBUG: ❌ {error_msg}")
            return self._get_fallback_response(
                "An error occurred while generating response.",
                language,
            )

    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt for the model."""
        prompts = {
            "en": "You are StudTor, an AI learning companion. Help students understand concepts clearly with examples and structured explanations.",
            "es": "Eres StudTor, un asistente de aprendizaje por IA. Ayuda a los estudiantes a entender conceptos claramente con ejemplos y explicaciones estructuradas.",
            "fr": "Vous êtes StudTor, un assistant d'apprentissage par IA. Aidez les étudiants à comprendre les concepts clairement avec des exemples et des explications structurées.",
            "de": "Du bist StudTor, ein KI-Lernbegleiter. Helfe Studierenden, Konzepte klar zu verstehen, mit Beispielen und strukturierten Erklärungen.",
            "pt": "Você é StudTor, um assistente de aprendizagem por IA. Ajude os alunos a entender conceitos claramente com exemplos e explicações estruturadas.",
            "hi": "आप StudTor हैं, एक AI सीखने का साथी। छात्रों को उदाहरणों और संरचित व्याख्याओं के साथ अवधारणाओं को स्पष्ट रूप से समझने में मदद करें।",
        }
        return prompts.get(language, prompts["en"])

    def _get_fallback_response(self, error: str, language: str) -> str:
        """Get fallback response when Ollama is not available."""
        fallbacks = {
            "en": f"Local AI is not ready. {error} Please check the backend logs for details.",
            "es": f"La IA local no está lista. {error} Verifique los registros del backend para más detalles.",
            "fr": f"L'IA locale n'est pas prête. {error} Veuillez vérifier les journaux du backend pour plus de détails.",
            "de": f"Die lokale KI ist nicht bereit. {error} Bitte überprüfen Sie die Backend-Protokolle für weitere Details.",
            "pt": f"A IA local não está pronta. {error} Verifique os registros do backend para mais detalhes.",
            "hi": f"स्थानीय AI तैयार नहीं है। {error} विवरण के लिए बैकएंड लॉग की जांच करें।",
        }
        return fallbacks.get(language, fallbacks["en"])
