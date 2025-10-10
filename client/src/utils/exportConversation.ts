/**
 * Conversation Export Utilities
 * Modular functions for exporting Safety Copilot conversations
 */

interface ConversationMessage {
    id: string;
    question: string;
    dataset: string;
    toolCalls: any[];
    analysis: string;
    response: any;
    timestamp: number;
  }
  
  interface ExportOptions {
    conversationHistory: ConversationMessage[];
    persona: string;
    onSuccess: (message: string) => void;
    onError: (error: string) => void;
  }
  
  /**
   * Map persona ID to display name
   */
  const getPersonaDisplayName = (persona: string): string => {
    const personaNames: Record<string, string> = {
      'default': 'General User',
      'mike': 'Field Operator',
      'safeer': 'Safety Engineer',
      'sarah': 'Safety Manager',
      'david': 'Site Head'
    };
    return personaNames[persona] || 'General User';
  };
  
  /**
   * Helper to download file
   */
  const downloadFile = (filename: string, content: string, type: string) => {
    try {
      const blob = new Blob([content], { type });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Failed to download file:', e);
      throw e;
    }
  };
  
  /**
   * Convert markdown-style formatting to plain text for MD export
   */
  const formatTextForMarkdown = (text: string): string => {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '**$1**')  // Keep bold
      .replace(/\*(.*?)\*/g, '*$1*')        // Keep italic
      .trim();
  };
  
  /**
   * Convert markdown-style formatting to HTML
   */
  const formatTextForHTML = (text: string): string => {
    if (!text) return '';
    
    let formatted = text;
    
    // Convert markdown tables to HTML
    const tableRegex = /(\|[^\n]+\|\r?\n)((?:\|[-:\s|]+\|\r?\n))?((?:\|[^\n]+\|\r?\n?)+)/g;
    formatted = formatted.replace(tableRegex, (match, header, separator, body) => {
      const headerCells = header.split('|').filter(cell => cell.trim()).map(cell => 
        `<th>${cell.trim()}</th>`
      ).join('');
      
      const bodyRows = body.trim().split('\n').map(row => {
        const cells = row.split('|').filter(cell => cell.trim()).map(cell => 
          `<td>${cell.trim()}</td>`
        ).join('');
        return `<tr>${cells}</tr>`;
      }).join('');
      
      return `<table><thead><tr>${headerCells}</tr></thead><tbody>${bodyRows}</tbody></table>`;
    });
    
    formatted = formatted
      // Convert headers
      .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
      .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
      .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
      // Convert bold and italic
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Convert bullet lists
      .replace(/^[\-\*]\s+(.+)$/gm, '<li>$1</li>')
      // Convert numbered lists
      .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>')
      // Convert line breaks
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');
    
    // Wrap list items in ul tags
    formatted = formatted.replace(/(<li>.*?<\/li>)/gs, (match) => {
      if (!match.includes('<ul>') && !match.includes('<ol>')) {
        return '<ul>' + match + '</ul>';
      }
      return match;
    });
    
    // Wrap in paragraph tags if not already wrapped
    if (!formatted.startsWith('<h') && !formatted.startsWith('<ul>') && !formatted.startsWith('<table>')) {
      formatted = '<p>' + formatted + '</p>';
    }
    
    // Clean up empty paragraphs
    formatted = formatted.replace(/<p><\/p>/g, '').replace(/<p>\s*<\/p>/g, '');
    
    return formatted;
  };
  
  /**
   * Escape HTML special characters
   */
  const escapeHTML = (text: string): string => {
    if (!text) return '';
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };
  
  /**
   * Export conversation as Markdown
   */
  export const exportAsMarkdown = ({ conversationHistory, persona, onSuccess, onError }: ExportOptions) => {
    if (conversationHistory.length === 0) {
      onError("No conversation to export");
      return;
    }
  
    const timestamp = new Date().toISOString();
    const date = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    const time = new Date().toLocaleTimeString('en-US');
  
    let markdown = `# Safety Copilot - Conversation Export
  
  ---
  
  ## Metadata
  
  | Field | Value |
  |-------|-------|
  | **Export Date** | ${date} |
  | **Export Time** | ${time} |
  | **Total Messages** | ${conversationHistory.length} |
  | **Persona** | ${getPersonaDisplayName(persona)} |
  
  ---
  
  `;
  
    // Add conversation messages
    conversationHistory.forEach((msg, index) => {
      const msgDate = new Date(msg.timestamp).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
  
      markdown += `## Message ${index + 1}\n\n`;
      markdown += `> **Timestamp:** ${msgDate}  \n`;
      markdown += `> **Dataset:** ${msg.dataset}\n\n`;
      
      // User Question
      markdown += `### Question\n\n`;
      markdown += `${formatTextForMarkdown(msg.question)}\n\n`;
      
      // AI Response
      markdown += `### Response\n\n`;
      const formattedAnalysis = formatTextForMarkdown(msg.analysis || 'No analysis available');
      markdown += `${formattedAnalysis}\n\n`;
      
      // Chart/Figure (if any)
      if (msg.response?.mpl_png_base64) {
        markdown += `### Visualization\n\n`;
        markdown += `![Chart for Message ${index + 1}](data:image/png;base64,${msg.response.mpl_png_base64})\n\n`;
      }
  
      markdown += `---\n\n`;
    });
  
    // Add footer
    markdown += `## Notes\n\n`;
    markdown += `This conversation was exported from **Safety Copilot** - AI-powered workplace safety analysis.\n\n`;
    markdown += `- **Export ID:** \`${timestamp}\`\n`;
    markdown += `- **Generated by:** Qbit Dynamics\n\n`;
    markdown += `### Disclaimer\n\n`;
    markdown += `AI-generated insights should be reviewed by qualified safety professionals before implementation.\n`;
  
    // Download the file
    const filename = `safety-copilot-conversation-${new Date().toISOString().split('T')[0]}.md`;
    
    try {
      downloadFile(filename, markdown, 'text/markdown;charset=utf-8');
      onSuccess(`${conversationHistory.length} messages exported as ${filename}`);
    } catch (error) {
      onError("Could not export conversation as Markdown");
    }
  };
  
  /**
   * Export conversation as HTML
   */
  export const exportAsHTML = ({ conversationHistory, persona, onSuccess, onError }: ExportOptions) => {
    if (conversationHistory.length === 0) {
      onError("No conversation to export");
      return;
    }
  
    const timestamp = new Date().toISOString();
    const date = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    const time = new Date().toLocaleTimeString('en-US');
  
    let html = `<!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Safety Copilot - Conversation Export</title>
      <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          :root {
            --bg: #ffffff;
            --fg: #111111;
            --muted: #666666;
            --border: #e5e7eb;
            --card: #fafafa;
            --radius: 10px;
            --container: 880px;
          }
          body {
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji';
            line-height: 1.65;
            color: var(--fg);
            background: var(--bg);
            padding: 32px;
          }
          .container {
            max-width: var(--container);
            margin: 0 auto;
          }
          .header {
            margin: 0 0 24px 0;
            padding: 0;
          }
          .header h1 {
            font-size: 22px;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: var(--fg);
          }
          .metadata {
            background: #fff;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 16px 20px;
            margin-bottom: 16px;
          }
          .metadata-grid {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
              gap: 12px 16px;
          }
          .metadata-item {
              display: flex;
              flex-direction: column;
          }
          .metadata-label {
              font-size: 12px;
              color: var(--muted);
              text-transform: uppercase;
              letter-spacing: .04em;
              margin-bottom: 4px;
              font-weight: 500;
          }
          .metadata-value {
              font-size: 14px;
              font-weight: 600;
              color: var(--fg);
          }
          .messages {
              padding: 0;
          }
          .message {
              margin-bottom: 16px;
              border: 1px solid var(--border);
              border-radius: var(--radius);
              padding: 16px;
              position: relative;
          }
          .message:last-child {
              margin-bottom: 0;
          }
          .message-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: 12px;
              padding-bottom: 8px;
              border-bottom: 1px solid var(--border);
          }
          .message-number {
              font-size: 14px;
              font-weight: 600;
              color: var(--fg);
          }
          .message-info {
              text-align: right;
          }
          .message-timestamp {
              display: block;
              font-size: 12px;
              color: var(--muted);
              margin-bottom: 2px;
          }
          .message-dataset {
              display: inline-block;
              background: var(--card);
              color: #4b5563;
              padding: 2px 8px;
              border: 1px solid var(--border);
              border-radius: 9999px;
              font-size: 12px;
              font-weight: 500;
          }
          .question {
              background: var(--card);
              padding: 14px;
              border-radius: 8px;
              margin-bottom: 12px;
              border: 1px solid var(--border);
          }
          .question-label {
              font-size: 12px;
              color: var(--muted);
              text-transform: uppercase;
              margin-bottom: 8px;
              font-weight: 600;
              letter-spacing: .04em;
          }
          .question-text {
              font-size: 14px;
              color: var(--fg);
              font-weight: 500;
              line-height: 1.6;
          }
          .response {
              padding: 16px;
              background: #ffffff;
              border-radius: 8px;
              border: 1px solid var(--border);
          }
          .response-label {
              font-size: 12px;
              color: var(--muted);
              text-transform: uppercase;
              margin-bottom: 10px;
              font-weight: 600;
              letter-spacing: .04em;
          }
          .response-text {
              color: #374151;
              line-height: 1.75;
          }
          .response-text p {
              margin-bottom: 12px;
          }
          .response-text h1,
          .response-text h2,
          .response-text h3 {
              margin-top: 20px;
              margin-bottom: 10px;
              color: var(--fg);
              font-weight: 600;
          }
          .response-text h1 { font-size: 20px; }
          .response-text h2 { font-size: 18px; }
          .response-text h3 { font-size: 16px; }
          .response-text ul, 
          .response-text ol {
              margin-left: 20px;
              margin-top: 8px;
              margin-bottom: 12px;
          }
          .response-text li {
              margin-bottom: 6px;
              line-height: 1.6;
          }
          .response-text strong {
              color: var(--fg);
              font-weight: 600;
          }
          .response-text em {
              font-style: italic;
              color: #4b5563;
          }
          .response-text table {
              width: 100%;
              border-collapse: collapse;
              margin: 12px 0;
              background: #ffffff;
              border: 1px solid var(--border);
              border-radius: 6px;
              overflow: hidden;
          }
          .response-text thead {
              background: #fafafa;
          }
          .response-text th {
              padding: 10px 12px;
              text-align: left;
              font-weight: 600;
              color: #374151;
              border-bottom: 1px solid var(--border);
              font-size: 12px;
              text-transform: uppercase;
              letter-spacing: .04em;
          }
          .response-text td {
              padding: 10px 12px;
              border-bottom: 1px solid var(--border);
              color: #374151;
          }
          .response-text tbody tr:last-child td {
              border-bottom: none;
          }
          .response-text tbody tr:hover {
              background: #fafafa;
          }
          .chart {
              margin-top: 12px;
              padding: 12px;
              background: #fff;
              border: 1px solid var(--border);
              border-radius: 8px;
              text-align: center;
          }
          .chart-label {
              font-size: 12px;
              color: var(--muted);
              text-transform: uppercase;
              margin-bottom: 8px;
              font-weight: 600;
              letter-spacing: .04em;
          }
          .chart img {
              max-width: 100%;
              height: auto;
              border-radius: 6px;
              border: 1px solid var(--border);
          }
          .footer {
              background: transparent;
              padding: 24px 0;
              text-align: center;
              color: var(--muted);
              border-top: 1px solid var(--border);
          }
          .footer-content {
              margin-bottom: 20px;
          }
          .footer-content p {
              margin-bottom: 6px;
              font-size: 14px;
          }
          .footer-content strong {
              color: var(--fg);
          }
          .export-id {
              font-size: 12px;
              color: #9ca3af;
              font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
              margin-top: 8px;
          }
          .disclaimer {
              background: var(--card);
              border: 1px solid var(--border);
              color: #4b5563;
              padding: 12px;
              border-radius: 8px;
              margin-top: 16px;
              font-size: 13px;
              line-height: 1.6;
          }
          .disclaimer strong {
              display: block;
              margin-bottom: 6px;
              font-size: 13px;
          }
          @media print {
              body { 
                  background: white; 
                  padding: 0; 
              }
              .container { 
                  max-width: 100%;
              }
              .message {
                  page-break-inside: avoid;
              }
          }
          @media (max-width: 768px) {
              .metadata-grid {
                  grid-template-columns: 1fr;
              }
              .message-header {
                  flex-direction: column;
                  align-items: flex-start;
              }
              .message-info {
                  text-align: left;
                  margin-top: 10px;
              }
          }
      </style>
  </head>
  <body>
      <div class="container">
          <div class="header">
              <h1>Safety Copilot — Conversation Export</h1>
          </div>
          
          <div class="metadata">
              <div class="metadata-grid">
                  <div class="metadata-item">
                      <span class="metadata-label">Export Date</span>
                      <span class="metadata-value">${date}</span>
                  </div>
                  <div class="metadata-item">
                      <span class="metadata-label">Export Time</span>
                      <span class="metadata-value">${time}</span>
                  </div>
                  <div class="metadata-item">
                      <span class="metadata-label">Total Messages</span>
                      <span class="metadata-value">${conversationHistory.length}</span>
                  </div>
                  <div class="metadata-item">
                      <span class="metadata-label">Persona</span>
                      <span class="metadata-value">${getPersonaDisplayName(persona)}</span>
                  </div>
              </div>
          </div>
          
          <div class="messages">`;
  
    conversationHistory.forEach((msg, index) => {
      const msgDate = new Date(msg.timestamp).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
  
      // Escape and format the question
      const questionText = escapeHTML(msg.question);
      
      // Format and escape the analysis
      const rawAnalysis = msg.analysis || 'No analysis available';
      const formattedAnalysis = formatTextForHTML(escapeHTML(rawAnalysis));
  
      html += `
              <div class="message">
                  <div class="message-header">
                      <span class="message-number">Message ${index + 1}</span>
                      <div class="message-info">
                          <span class="message-timestamp">${msgDate}</span>
                          <span class="message-dataset">${escapeHTML(msg.dataset)}</span>
                      </div>
                  </div>
                  
                  <div class="question">
                      <div class="question-label">Question</div>
                      <div class="question-text">${questionText}</div>
                  </div>
                  
                  <div class="response">
                      <div class="response-label">Response</div>
                      <div class="response-text">${formattedAnalysis}</div>
                  </div>`;
  
      if (msg.response?.mpl_png_base64) {
        html += `
                  <div class="chart">
                      <div class="chart-label">Visualization</div>
                      <img src="data:image/png;base64,${msg.response.mpl_png_base64}" alt="Chart for Message ${index + 1}">
                  </div>`;
      }
  
      html += `
              </div>`;
    });
  
    html += `
          </div>
          
          <div class="footer">
              <div class="footer-content">
                  <p><strong>Safety Copilot</strong> - AI-powered workplace safety analysis</p>
                  <p>Generated by <strong>Qbit Dynamics</strong></p>
                  <div class="export-id">Export ID: ${timestamp}</div>
              </div>
              <div class="disclaimer">
                  <strong>Disclaimer</strong>
                  AI-generated insights should be reviewed by qualified safety professionals before implementation.
              </div>
          </div>
      </div>
  </body>
  </html>`;
  
    const filename = `safety-copilot-conversation-${new Date().toISOString().split('T')[0]}.html`;
    
    try {
      downloadFile(filename, html, 'text/html;charset=utf-8');
      onSuccess(`${conversationHistory.length} messages exported as ${filename}`);
    } catch (error) {
      onError("Could not export conversation as HTML");
    }
  };