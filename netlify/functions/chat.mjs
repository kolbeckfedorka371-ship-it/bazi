// Netlify Function: AI 命理问答代理
// API Key 仅存于此，永远不会发送到浏览器

const API_KEY = "sk-c96f3f7044e34a70be197a2b1270fd52";
const API_URL = "https://api.deepseek.com/v1/chat/completions";

export default async (req) => {
  // 只允许 POST
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const body = await req.json();
    const { messages } = body;

    if (!messages || !Array.isArray(messages)) {
      return new Response(JSON.stringify({ error: "Invalid request: messages required" }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const resp = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: "deepseek-chat",
        messages: messages,
        max_tokens: 1200,
        temperature: 0.7
      })
    });

    const data = await resp.json();

    if (!resp.ok) {
      return new Response(JSON.stringify({
        error: true,
        message: data.error?.message || "AI 服务暂不可用"
      }), {
        status: resp.status,
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response(JSON.stringify({
      success: true,
      content: data.choices?.[0]?.message?.content || ""
    }), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      error: true,
      message: "服务器异常: " + err.message
    }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
};
