# LazyTradie Admin Copilot: Every Line

**18 files to make**, one per line, exactly as written. Save each to `copilot/assets/vo/` with the
file name shown (MP3 or WAV). Pauses and timing are handled in the edit.

---

## 1. Narrator (2 lines): the explainer's narrator voice in ElevenLabs
The same voice and settings as the explainer, so the series sounds like one product.
**LazyTradie** = LAY-zee TRAY-dee.

| File | Line |
|---|---|
| `N_01` | Everything you're about to see gets done by voice. No typing. No tapping. Just LazyTradie Copilot. |
| `N_02` | Your schedule. Your jobs. Your quotes and invoices… sorted. Just by asking. |

```
Everything you're about to see gets done by voice. No typing. No tapping. Just LazyTradie Copilot.
```
```
Your schedule. Your jobs. Your quotes and invoices… sorted. Just by asking.
```

---

## 2. Jack, the tradie (8 lines): ElevenLabs
**Voice brief:** an Australian male, mid 30s to 40s, relaxed and casual, a little gravelly, talking
to his phone between jobs. He's not performing or announcing. Natural pace, and the short ones are
short. I'll add the phone-mic feel in the mix, so generate it clean.

| File | Line |
|---|---|
| `TR_01` | What's on today? |
| `TR_02` | Find Sarah's switchboard job. |
| `TR_03` | Approve it, and move it to Friday at two. |
| `TR_04` | Book Mike Chen tomorrow at ten. Two downlights, Smith Street, Fitzroy. |
| `TR_05` | Yep. |
| `TR_06` | Add a note to Mike's job… bring the long ladder. |
| `TR_07` | Quote Sarah for the switchboard upgrade. |
| `TR_08` | Invoice Liam's job from this morning. |

---

## 3. Copilot (8 lines): Deepgram TTS, voice **Sharon** (`flux-sharon-en`)
This is the real voice the Copilot speaks with in Talk mode. For pauses, use a single **…**
character or a full stop. Three typed dots ("...") come out erratic with Sharon.

| File | Line |
|---|---|
| `CV_01` | Pulling up today… You've got four jobs. First up, Liam in Richmond at 8. |
| `CV_02` | Finding Sarah's job… Switchboard upgrade in Hawthorn, Thursday at 9. It's waiting on your approval. |
| `CV_03` | Updating that… Approved, and moved to Friday at 2 PM. |
| `CV_04` | Book Mike, two downlights, Smith St Fitzroy, tomorrow at 10 AM? |
| `CV_05` | Booked in for tomorrow at 10. |
| `CV_06` | Adding that note… Done. It's on Mike's job. |
| `CV_07` | Drafting Sarah's quote… $2,450 for the switchboard upgrade. Tap confirm to send. |
| `CV_08` | Checking Liam's job… Invoice drafted, $380. Tap confirm to send. |

**Already have (real product recordings, nothing to make):**
- `CV_00` "Morning! What can I sort out for you?" opens the conversation.
- `CV_09` "Afternoon, mate. What's next on the list?" plays over the end card.

---

**Running order:** N_01 · CV_00 · TR_01 · CV_01 · TR_02 · CV_02 · TR_03 · CV_03 · TR_04 · CV_04 ·
TR_05 · CV_05 · TR_06 · CV_06 · TR_07 · CV_07 · TR_08 · CV_08 · N_02 · CV_09
