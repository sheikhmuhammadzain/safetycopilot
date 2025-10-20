# Testing Guide: Message Saving Fixes

## Quick Test Scenarios

### Scenario 1: Basic Message Save
**Expected**: Message appears once in history, no duplicates

1. Open the Safety Copilot agent page
2. Open browser DevTools Console (F12)
3. Send any question (e.g., "Show me incident trends")
4. Watch the console logs:
   ```
   ✅ Look for:
   - 🆕 New message ID: msg_...
   - 💾 Persisting message: [id]
   - ✅ Message updated to complete with analysis length: [number]
   - ✅ Message marked as saved in ref
   
   ❌ Should NOT see:
   - Multiple "Persisting message" with same ID
   - "Adding new message to history" after "Updating existing message"
   ```
5. Verify: Only ONE message appears in the conversation history

---

### Scenario 2: Current Message Visibility
**Expected**: Current message smoothly transitions to history

1. Send a question
2. Watch the current message as it streams
3. When streaming completes:
   - ✅ Current message should remain visible
   - ✅ Message should then appear in history above
   - ✅ Current message should disappear only after appearing in history
   - ❌ Should NOT flicker or disappear prematurely

---

### Scenario 3: Multiple Messages Rapidly
**Expected**: All messages saved correctly, no duplicates

1. Send message #1: "Show me incidents"
2. Wait for response
3. Immediately send message #2: "Show me hazards"
4. Wait for response
5. Send message #3: "Create a chart"
6. Check console logs:
   ```
   ✅ Each message should have:
   - Unique ID
   - Single persist call per message
   - No "already persisted, skipping" for first save
   ```
7. Verify: Exactly 3 messages in history (no duplicates)

---

### Scenario 4: Stop Streaming Mid-Response
**Expected**: Partial message saved correctly

1. Send a complex question (e.g., "Analyze all incidents with charts")
2. Click STOP button mid-stream (around 2-3 seconds)
3. Check console:
   ```
   ✅ Should see:
   - Message being persisted even though incomplete
   - Analysis saved with whatever was streamed
   ```
4. Verify: Message appears in history with partial content

---

### Scenario 5: Page Refresh Persistence
**Expected**: Conversation persists across page reloads

1. Send 2-3 messages
2. Wait for all responses to complete
3. Refresh the page (F5)
4. Check console:
   ```
   ✅ Should see:
   - 📚 Loaded [X] messages from storage
   ```
5. Verify: All previous messages appear in history

---

### Scenario 6: Network Error Handling
**Expected**: Message saved even if network fails

1. Open DevTools Network tab
2. Set throttling to "Offline" after sending message
3. Message should still save to localStorage
4. Refresh page
5. Verify: Message appears with error state but is saved

---

## Console Log Patterns

### ✅ Healthy Save Flow
```
🆕 New message ID: msg_1234567890_1_abc123
📡 WebSocket connected
📝 Agent memory: 3 recent messages (limit: 3)
[... streaming events ...]
🎯 Complete event received
💾 Persisting message: msg_1234567890_1_abc123 with analysis length: 532
📝 Persisting message: msg_1234567890_1_abc123 status: not-set
🔄 Updating existing message at index 0 from status: pending
✅ Message updated to complete with analysis length: 532
✅ Message marked as saved in ref
⏭️ Message already saved, skipping duplicate save: msg_1234567890_1_abc123
```

### ❌ Problematic Pattern (Should NOT Occur)
```
💾 Persisting message: msg_1234567890_1_abc123
💾 Persisting message: msg_1234567890_1_abc123  ❌ DUPLICATE!
➕ Adding new message to history  ❌ Should UPDATE, not ADD!
```

---

## Visual Checks

### Current Message UI
- [ ] Appears immediately when you send question
- [ ] Shows streaming response in real-time
- [ ] Has animated cursor during streaming
- [ ] Shows "Chain of thoughts" collapsible section
- [ ] Smoothly disappears when message moves to history
- [ ] NO flicker or premature disappearing

### History Messages
- [ ] Each message appears exactly once
- [ ] Messages maintain correct order (oldest to newest)
- [ ] Tool calls and charts preserved
- [ ] Analysis text complete and formatted
- [ ] Action buttons (copy, like, etc.) work
- [ ] Follow-up questions appear

### Memory Badge (Top Right)
- [ ] Shows "Memory: X/3" badge
- [ ] Updates correctly as conversation grows
- [ ] Tooltip shows correct information

---

## Edge Cases to Test

1. **Very Long Response**: Send "Analyze all incidents in detail with multiple charts"
   - Should save without truncation
   - Should not duplicate

2. **Empty Response**: Simulate backend returning empty analysis
   - Should save with "Analysis complete." fallback
   - Should not crash

3. **Rapid Fire**: Send 5 messages in quick succession
   - All should save
   - No ID collisions
   - Correct order maintained

4. **Browser Tab Switch**: Send message, switch tab mid-stream, return
   - Message should continue streaming
   - Should save when complete
   - Visibility change should trigger storage flush

---

## Success Criteria

- ✅ No duplicate messages in history
- ✅ No console errors
- ✅ Smooth UI transitions
- ✅ All messages persist across refresh
- ✅ Memory limit (3) respected
- ✅ localStorage size reasonable (<5MB for 20 messages)
- ✅ No "already persisted" warnings on first save
- ✅ Current message visible throughout streaming

## If Issues Persist

1. **Clear localStorage**: `localStorage.removeItem('safety-copilot-conversation')`
2. **Hard refresh**: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
3. **Check console for specific error messages**
4. **Verify backend is responding correctly** (WebSocket connection)
5. **Check Network tab for failed requests**

