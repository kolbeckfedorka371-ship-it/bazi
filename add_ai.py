import os

html_path = r'C:\Users\ASUS\bazi-website\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add AI card to home page
old_card = '      <div class="module-card" onclick="showView(\'marriage\')" style="border-color:rgba(236,72,153,0.2)">\n        <span class="icon">💕</span>\n        <h2>合婚配对</h2>\n        <p>双人八字，五行互补，姻缘评分</p>\n      </div>\n    </div>'

new_card = '''      <div class="module-card" onclick="showView('marriage')" style="border-color:rgba(236,72,153,0.2)">
        <span class="icon">💕</span>
        <h2>合婚配对</h2>
        <p>双人八字，五行互补，姻缘评分</p>
      </div>
      <div class="module-card" onclick="showView('ai')" style="border-color:rgba(59,130,246,0.2)">
        <span class="icon">🤖</span>
        <h2>AI 命理解读</h2>
        <p>DeepSeek R1 智能问答，命理深度分析</p>
      </div>
    </div>'''

content = content.replace(old_card, new_card)

# 2. Add AI view HTML
ai_view = '''
  <div class="view" id="view-ai">
    <div class="glass-panel" style="border-color:rgba(59,130,246,0.2)">
      <h3 style="background:linear-gradient(180deg,#60a5fa 20%,#3b82f6 80%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-size:2rem;letter-spacing:0.15em">AI 命理解读</h3>
      <p class="text-muted mb-16" style="font-family:'ZCOOL XiaoWei',serif;font-size:15px;letter-spacing:0.08em">
        DeepSeek R1 智能命理助手，随时为你解答命理疑惑
      </p>
      <div id="ai-chat-messages" style="height:400px;overflow-y:auto;padding:16px;background:rgba(0,0,0,0.2);border-radius:12px;margin-bottom:16px;border:1px solid rgba(59,130,246,0.1)">
        <div style="text-align:center;color:rgba(200,200,220,0.4);font-size:13px;padding:40px 0">
          <div style="font-size:48px;margin-bottom:12px">🤖</div>
          你好！我是 AI 命理助手，基于 DeepSeek R1 模型。<br>
          你可以问我关于八字、命理、运势、风水等任何问题。<br>
          <span style="font-size:11px;color:rgba(200,200,220,0.3)">例如：我的八字五行缺什么？今天适合做什么？</span>
        </div>
      </div>
      <div style="display:flex;gap:12px">
        <input type="text" id="ai-input" class="ly-question" style="flex:1;margin:0;max-width:none;text-align:left" placeholder="输入你的命理问题..." onkeypress="if(event.key==='Enter')sendAIMessage()">
        <button class="btn" style="padding:12px 24px;white-space:nowrap;background:linear-gradient(135deg,#3b82f6,#2563eb)" onclick="sendAIMessage()">发送</button>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="reset-btn" style="font-size:12px;padding:6px 12px;background:rgba(59,130,246,0.1);border-color:rgba(59,130,246,0.3);color:#60a5fa" onclick="askAI('帮我分析一下八字中五行缺什么，该怎么补？')">五行分析</button>
        <button class="reset-btn" style="font-size:12px;padding:6px 12px;background:rgba(59,130,246,0.1);border-color:rgba(59,130,246,0.3);color:#60a5fa" onclick="askAI('最近运势如何？有什么需要注意的？')">运势分析</button>
        <button class="reset-btn" style="font-size:12px;padding:6px 12px;background:rgba(59,130,246,0.1);border-color:rgba(59,130,246,0.3);color:#60a5fa" onclick="askAI('我的事业发展方向应该如何选择？')">事业指导</button>
        <button class="reset-btn" style="font-size:12px;padding:6px 12px;background:rgba(59,130,246,0.1);border-color:rgba(59,130,246,0.3);color:#60a5fa" onclick="askAI('我的感情运势如何？什么时候会遇到对的人？')">感情运势</button>
      </div>
    </div>
  </div>'''

# Insert before closing </div></div> before <script>
content = content.replace('</div>\n</div>\n\n<script>', '</div>\n' + ai_view + '\n</div>\n\n<script>', 1)

# 3. Add AI JS functions
ai_js = r'''
// ===================== AI CHAT MODULE =====================
const AI_SYSTEM_PROMPT = "你是一个专业的中国传统命理分析AI助手，精通八字命理、紫微斗数、梅花易数、六爻占卜、黄历择吉、塔罗牌解读。你的回答应该：1. 基于中国传统命理学原理，给出专业、准确的分析；2. 语言风格温和、有智慧，带有传统命理师的口吻；3. 给出实用的建议，帮助用户趋吉避凶；4. 回答要详细但不冗长，300字以内；5. 使用适当的 emoji 让回答更生动。";

let aiConversationHistory = [{role: 'system', content: AI_SYSTEM_PROMPT}];

function addChatMessage(role, content) {
  const messagesDiv = document.getElementById('ai-chat-messages');
  const isUser = role === 'user';
  const msg = document.createElement('div');
  msg.style.cssText = 'display:flex;justify-content:' + (isUser?'flex-end':'flex-start') + ';margin-bottom:12px;';
  const bubble = document.createElement('div');
  bubble.style.cssText = 'max-width:80%;padding:12px 16px;border-radius:16px;font-size:14px;line-height:1.8;white-space:pre-wrap;word-break:break-word;' + (isUser ? 'background:linear-gradient(135deg,#3b82f6,#2563eb);color:white;border-bottom-right-radius:4px;' : 'background:rgba(59,130,246,0.08);color:rgba(240,214,138,0.9);border:1px solid rgba(59,130,246,0.15);border-bottom-left-radius:4px;');
  bubble.textContent = content;
  if (!isUser) {
    const label = document.createElement('div');
    label.style.cssText = 'font-size:11px;color:rgba(59,130,246,0.6);margin-bottom:4px;font-weight:600;';
    label.textContent = 'AI 命理助手';
    msg.appendChild(label);
  }
  msg.appendChild(bubble);
  messagesDiv.appendChild(msg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function askAI(question) {
  document.getElementById('ai-input').value = question;
  sendAIMessage();
}

async function sendAIMessage() {
  const input = document.getElementById('ai-input');
  const question = input.value.trim();
  if (!question) return;
  input.value = '';
  addChatMessage('user', question);
  aiConversationHistory.push({role: 'user', content: question});
  const messagesDiv = document.getElementById('ai-chat-messages');
  const loadingMsg = document.createElement('div');
  loadingMsg.style.cssText = 'display:flex;justify-content:flex-start;margin-bottom:12px;';
  loadingMsg.innerHTML = '<div style="padding:12px 16px;background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.15);border-radius:16px;border-bottom-left-radius:4px;color:rgba(200,200,220,0.5);font-size:14px">AI 思考中...</div>';
  messagesDiv.appendChild(loadingMsg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  try {
    const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-onwtR2fRXq14NsvPQyPRe5X85MipKZt44gu8M3WJ7VCKrxqk'
      },
      body: JSON.stringify({
        model: 'deepseek-ai/DeepSeek-R1',
        messages: aiConversationHistory,
        max_tokens: 1024,
        temperature: 0.7,
        stream: false
      })
    });
    loadingMsg.remove();
    if (!response.ok) throw new Error('API error: ' + response.status);
    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || '抱歉，我暂时无法回答这个问题。';
    const cleanReply = reply.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
    addChatMessage('assistant', cleanReply);
    aiConversationHistory.push({role: 'assistant', content: cleanReply});
    if (aiConversationHistory.length > 20) {
      aiConversationHistory = [aiConversationHistory[0], ...aiConversationHistory.slice(-10)];
    }
  } catch (error) {
    loadingMsg.remove();
    addChatMessage('assistant', '抱歉，AI 服务暂时不可用，请稍后再试。');
    console.error('AI Error:', error);
  }
}
'''

content = content.replace('// ===================== INIT =====================', ai_js + '\n// ===================== INIT =====================')

# 4. Add showView handler
old_sv = "else if(name==='marriage'){document.title='合婚配对 - 命理玄学';resetMarriage()}"
new_sv = "else if(name==='marriage'){document.title='合婚配对 - 命理玄学';resetMarriage()}\n    else if(name==='ai'){document.title='AI命理解读 - 命理玄学';setTimeout(()=>document.getElementById('ai-input').focus(),100)}"
content = content.replace(old_sv, new_sv)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'AI module added. File size: {len(content):,} bytes')
