# Available Gemini Models (Daleel Petroleum Intelligence Hub)

This document lists the available models retrieved directly from your Gemini API project as of January 26, 2026.

---

## 🚀 Recommended Production Models
These are the most stable choices for "Agentic AI" reasoning.

| Model ID | Description |
| :--- | :--- |
| **`gemini-2.0-flash`** | Best overall balance of speed, intelligence, and free-tier quota. |
| **`gemini-2.5-flash`** | Higher intelligence Flash model for faster reasoning. |
| **`gemini-flash-latest`** | Points to the most recent stable Flash version. |
| **`gemini-pro-latest`** | Points to the most recent stable Pro version (High intelligence). |

---

## 🧪 Preview & Experimental Models
Use these for testing the "Cutting Edge" features, but beware of stricter rate limits.

| Model ID | Notes |
| :--- | :--- |
| **`gemini-3-flash-preview`** | The newest architecture (Flash version). |
| **`gemini-3-pro-preview`** | The newest architecture (Pro version). |
| **`gemini-exp-1206`** | High-utility experimental reasoning model. |
| **`gemini-2.5-computer-use-preview`** | Specialized for computer interaction tasks. |
| **`deep-research-pro-preview`** | Optimized for long-form synthesis and research. |

---

## ⚡ Lite & Efficient Models
Best for simple summarization or high-volume tasks.

| Model ID |
| :--- |
| **`gemini-2.0-flash-lite`** |
| **`gemini-2.5-flash-lite`** |
| **`gemini-flash-lite-latest`** |

---

## 🏗️ Specialized Architecture
Models for embeddings, images, or specific hardware.

- **Image Generation**: `gemini-2.0-flash-exp-image-generation`
- **Native Audio**: `gemini-2.5-flash-native-audio-latest`
- **Embeddings**: `text-embedding-004`, `gemini-embedding-001`
- **Lightweight**: `gemma-3-1b-it`, `gemma-3-27b-it` (The newest Gemma open-weights)

---

## 🛠️ How to Update
To switch models, edit the `config.yaml` file:

```yaml
llm:
  gemini:
    model: gemini-2.0-flash  # Replace with the Model ID of your choice
```
