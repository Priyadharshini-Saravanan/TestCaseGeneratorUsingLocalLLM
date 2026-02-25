/**
 * Chat UI Logic — Test Case Generator
 * Handles message send/receive, streaming, and UI state management.
 */

// --- DOM Elements ---
const chatContainer = document.getElementById("chat-container");
const messagesArea = document.getElementById("messages-area");
const welcomeSection = document.getElementById("welcome-section");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const charCount = document.getElementById("char-count");
const statusDot = document.getElementById("status-indicator");
const statusText = document.getElementById("status-text");

// --- State ---
let isGenerating = false;

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
    setupTextarea();
    // Health check every 30 seconds
    setInterval(checkHealth, 30000);
});

// --- Health Check ---
async function checkHealth() {
    try {
        const res = await fetch("/api/health");
        const data = await res.json();

        if (data.healthy) {
            statusDot.className = "status-dot status-connected";
            statusText.textContent = "Connected";
            statusDot.title = data.message;
        } else {
            statusDot.className = "status-dot status-disconnected";
            statusText.textContent = "Model unavailable";
            statusDot.title = data.message;
        }
    } catch (err) {
        statusDot.className = "status-dot status-disconnected";
        statusText.textContent = "Disconnected";
        statusDot.title = "Cannot reach server";
    }
}

// --- Textarea Auto-resize ---
function setupTextarea() {
    userInput.addEventListener("input", () => {
        // Auto-resize
        userInput.style.height = "auto";
        userInput.style.height = Math.min(userInput.scrollHeight, 150) + "px";

        // Character count
        const len = userInput.value.length;
        charCount.textContent = `${len} / 5000`;

        // Enable/disable send button
        sendBtn.disabled = len === 0 || isGenerating;
    });

    // Send on Enter (Shift+Enter for newline)
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (!isGenerating && userInput.value.trim()) {
                sendMessage();
            }
        }
    });
}

// --- Use Example ---
function useExample(btn) {
    userInput.value = btn.textContent;
    userInput.dispatchEvent(new Event("input"));
    userInput.focus();
}

// --- Send Message ---
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || isGenerating) return;

    // Hide welcome
    if (welcomeSection) {
        welcomeSection.style.display = "none";
    }

    // Add user message
    addMessage(text, "user");

    // Clear input
    userInput.value = "";
    userInput.style.height = "auto";
    charCount.textContent = "0 / 5000";
    sendBtn.disabled = true;
    isGenerating = true;

    // Add loading indicator
    const loadingEl = addLoadingMessage();

    try {
        // Use streaming endpoint
        const response = await fetch("/api/generate/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: text })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || "Server error");
        }

        // Remove loading indicator and create assistant message
        loadingEl.remove();
        const assistantEl = addMessage("", "assistant");
        const bubble = assistantEl.querySelector(".message-content");

        // Read the SSE stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullText = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split("\n");

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const data = line.slice(6);

                    if (data === "[DONE]") {
                        continue;
                    }

                    if (data.startsWith("[ERROR]")) {
                        throw new Error(data.slice(8));
                    }

                    fullText += data;
                    bubble.innerHTML = formatTestCases(fullText);
                    scrollToBottom();
                }
            }
        }

    } catch (err) {
        loadingEl.remove();
        addMessage(`Error: ${err.message}`, "error");
    } finally {
        isGenerating = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// --- Add Message to Chat ---
function addMessage(text, type) {
    const wrapper = document.createElement("div");
    wrapper.className = `message message-${type}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const content = document.createElement("div");
    content.className = "message-content";

    if (type === "user") {
        content.textContent = text;
    } else if (type === "error") {
        content.textContent = text;
    } else {
        content.innerHTML = formatTestCases(text);
        addCopyButtons(content);
    }

    bubble.appendChild(content);
    wrapper.appendChild(bubble);
    messagesArea.appendChild(wrapper);
    scrollToBottom();

    return wrapper;
}

// --- Loading Message ---
function addLoadingMessage() {
    const wrapper = document.createElement("div");
    wrapper.className = "message message-assistant";
    wrapper.id = "loading-message";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = `
        <div class="loading-dots">
            <span></span><span></span><span></span>
        </div>
        <div class="loading-text">Ollama is thinking...</div>
    `;

    wrapper.appendChild(bubble);
    messagesArea.appendChild(wrapper);
    scrollToBottom();

    return wrapper;
}

// --- Format Test Cases (card rendering) ---
function formatTestCases(text) {
    if (!text) return "";

    // Split by horizontal rules or TC headers
    const parts = text.split(/---|\*\*Test Case ID:\*\*/g);

    if (parts.length <= 1) {
        return renderMarkdown(text);
    }

    let html = "";

    // Process the first part (usually a summary)
    if (parts[0].trim()) {
        html += `<div class="summary-text">${renderMarkdown(parts[0])}</div>`;
    }

    // Process each test case card
    for (let i = 1; i < parts.length; i++) {
        let part = parts[i].trim();
        if (!part) continue;

        // Re-add the split header if it was "Test Case ID"
        if (text.includes("**Test Case ID:**")) {
            part = "**Test Case ID:** " + part;
        }

        html += `
            <div class="tc-card">
                <div class="tc-card-body">${renderMarkdown(part)}</div>
                <button class="tc-copy-btn" onclick="copyToClipboard(this)" title="Copy Test Case">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"></path>
                    </svg>
                    <span>Copy</span>
                </button>
            </div>
        `;
    }

    return html;
}

// --- Basic Markdown Rendering ---
function renderMarkdown(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, "<em>$1</em>")
        .replace(/^(\d+)\.\s+(.*)$/gm, '<div class="list-item"><span class="list-num">$1.</span> $2</div>')
        .replace(/\n/g, "<br>");
}

// --- Copy Functionality ---
function addCopyButtons(container) {
    // Buttons are already added in HTML string in formatTestCases
}

async function copyToClipboard(btn) {
    const card = btn.closest(".tc-card");
    const text = card.querySelector(".tc-card-body").innerText;

    try {
        await navigator.clipboard.writeText(text);
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>Copied!</span>
        `;
        btn.classList.add("copied");
        setTimeout(() => {
            btn.innerHTML = originalHtml;
            btn.classList.remove("copied");
        }, 2000);
    } catch (err) {
        console.error("Failed to copy: ", err);
    }
}

// --- Scroll to Bottom ---
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
