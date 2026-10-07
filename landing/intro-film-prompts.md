# SmartScout AI - "The Transfer Window" (calm edit)

Scroll-driven intro film for the SmartScout landing page. Seven legs of ONE continuous
camera move (no cuts), so the scroll-scrub engine can play it forward and backward and
hold any frame as a still. Each leg starts from the previous leg's actual last frame.

## Generation settings (every leg)

| Setting | Value |
|---|---|
| Model | Kling 3.0 (`kling3_0`) on Higgsfield. There is no "Fable" video model; Fable is a Claude model name. |
| Mode | `4k` (3840 x 2160), `sound: off`, `cfg_scale: 0.5` |
| Aspect / duration | 16:9, 6 seconds per leg (42 s of film) |
| Leg 1 input | `start_image` = the approved "Room" still |
| Legs 2-7 input | `start_image` = the exact last rendered frame of the previous leg |
| Legs 3 and 4 | also `end_image` = a still generated with GPT Image 2.5 (16:9, 2k, the previous frame as `image_references`), because only an image model spells on-screen text reliably. Kling animates between the two frames. |
| Cost | 36 credits per leg (252 for the film) |

## World grammar (identical preamble in every prompt)

> Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle
> horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key.
> Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen
> glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no
> camera shake, no cuts. No faces, no on-screen text, no logos, no readable lettering.

Three adaptations from the original shot list, all forced by the scrub engine:

1. The office is at dusk, not night, so the flight out of the window lands in golden hour
   without a lighting jump.
2. The corridor handshake is dropped. Two-person hand contact is the most artifact-prone
   shot in AI video, and the signature carries the same "certainty" beat.
3. Every word on screen (search text, card labels, wordmark, tagline) is HTML laid over the
   film, never rendered inside it. The interface in Act 2 is prompted as pure light.

---

## Clip 1 - The Room (Act 1) - 6 s

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no on-screen text, no logos, no readable lettering.

Dusk. A quiet executive office with floor-to-ceiling windows; far beyond the glass a lit football stadium glows against the last gold of the sky and a dark city. A single figure sits in a leather chair, seen only from behind, perfectly still, thinking. At the left edge a glass whiteboard carries a few soft handwritten marks that catch the amber light; a desk lamp is the only practical. Empty floor, no clutter. The camera begins at the back of the room and pushes in toward the chair and the window at an imperceptibly slow, constant pace, keeping the figure centred with generous negative space above and to the sides. The move never stops; the last second continues the same gentle forward drift.

Emotion: someone is in control, and nothing is urgent.

## Clip 2 - The Glass (Act 1 into Act 2) - 6 s

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no on-screen text, no logos, no readable lettering.

Continuing the same slow forward drift from the previous frame, the camera glides closer behind the seated figure and drifts gently to the left so the glass whiteboard passes in the foreground, slightly soft, its few handwritten strokes catching amber light while the distant stadium glows through the glass. The reflection of the window slides across the board. The figure remains still, centred, seen from behind. The camera then eases back to centre and tilts down a few degrees toward the desk, where a laptop screen waits, cool blue-white, its glow touching the edge of the hands. Constant speed, no pause, generous dark negative space on the right. The final second continues the same gentle forward drift, now descending slightly toward the desk.

Emotion: the preparation was done long before tonight.

## Clip 3 - The Search (Act 2) - 6 s

Production note: a plain video prompt produced "SmartScuut" and "SmartSouut". The fix is an
exact end frame. First generate the still (GPT Image 2.5, 16:9, 2k, leg 2's last frame as the
reference): *the same office, camera closer and lower over the right shoulder, the laptop screen
filling the centre of frame, a dark minimal interface with one rounded search bar containing exactly
the words "SmartScout AI" in crisp white sans-serif with a thin cursor after the final letter,
nothing else on the screen, hands resting on the keyboard lit by the cool glow.* Then the clip:

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no logos, no watermarks.

Continuing the same slow forward drift, the camera descends over the right shoulder of the seated figure toward the open laptop on the desk, so the dark screen grows to fill the centre of the frame. The screen shows a dark, minimal interface with a single empty search bar. Two hands rest on the keyboard, lit by the soft cool glow, and type unhurriedly: the words SmartScout AI appear in the search bar letter by letter in crisp white sans-serif, followed by a thin blinking cursor. Nothing else ever appears on the screen. Shallow depth of field keeps the keyboard and the search bar sharp while the room stays a soft navy blur with one amber lamp. The move ends exactly on the final frame, the camera settled over the shoulder with the completed words on the screen.

Emotion: the question is simple when you know what to ask.

## Clip 4 - The Shortlist (Act 2) - 6 s

Production note: same end-frame technique. The still (GPT Image 2.5, leg 3's end frame as the
reference): *the laptop screen filling almost the whole frame; the search bar reads "SmartScout AI";
below it three dark cards stacked with generous spacing: "Tomás Herrera / Centre-back, 21" with a
small round emerald badge "94", "Noah Lindqvist / Left-back, 23" with a muted grey badge "88",
"Kwame Asante / Striker, 19" with a muted grey badge "86"; crisp white sans-serif, nothing else on
the screen.* Then the clip:

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no logos, no watermarks.

The push-in continues until the laptop screen fills almost the entire frame. Below the search bar that reads SmartScout AI, three player cards fade in one after another, slowly and calmly, from top to bottom, each a clean dark card with a name, a position and age line, and a small round score badge on the right, the first badge emerald green and the other two muted grey. The text is crisp white sans-serif and perfectly legible. Nothing else appears on the screen. The glow of the screen stays soft and even. The camera keeps pushing in at the same constant pace and settles exactly on the final frame with all three cards fully visible.

Emotion: three names, no noise.

## Clip 5 - The Signature (Act 3) - 6 s

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no on-screen text, no logos, no readable lettering.

The dark laptop screen with its three cards blooms gently into soft white light, and out of that glow the camera continues the same slow forward drift as the scene resolves: a desk at dusk under a single amber lamp, a hand holding a fountain pen completing one unhurried stroke of a signature on a cream document, the ink catching the light. No readable text on the page. A second hand rests on the desk; no faces. Shallow depth of field, oval bokeh from city lights in the window beyond. The camera glides forward over the desk at constant speed and begins to lift, the floor-to-ceiling window and the distant glowing stadium rising into the upper half of the frame. The final second continues the forward drift, now rising toward the glass.

Emotion: certainty, not relief.

## Clip 6 - Through the Glass (Act 3 into Act 4) - 6 s

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no on-screen text, no logos, no readable lettering.

Continuing the same slow forward drift and gentle rise, the camera passes through the floor-to-ceiling window: a soft anamorphic flare slides across the glass as the reflection gives way, and the camera emerges into the open evening air. Below, a dark city spreads out under the last gold of the sky; ahead and below, the stadium glows warm, its floodlights on, the bowl filling the lower centre of frame and growing slowly. No buildings cross the centre of the frame. Constant speed, a graceful shallow descent toward the stadium, like a drone easing down. Haze softens the horizon. The final second continues the same gentle descent toward the stadium rim.

Emotion: the decision leaves the room and enters the world.

## Clip 7 - The Pitch (Act 4) - 6 s

Cinematic luxury brand film, 4K, pristine and grain-free. Anamorphic lens with gentle horizontal flares and oval bokeh, long-lens compression, deep shadows, a single warm key. Palette: deep navy and warm charcoal, soft amber practical light, cool blue-white screen glow. One continuous slow camera move at constant speed, locked exposure, no flicker, no camera shake, no cuts. No faces, no on-screen text, no logos, no readable lettering.

The same slow descent carries the camera over the stadium rim, past the floodlights, into the bowl: the stands are a sea of colour, patient and still, catching golden-hour light. The camera keeps descending toward the pitch and levels out low behind a single player in a plain kit, no crest and no number, walking slowly onto the pitch with a ball at their feet, seen only from behind. Long-lens compression stacks the crowd behind them. The camera eases to a complete, graceful stop with the player slightly below centre and clean sky and stands above. No celebration, just presence. The final frame holds still as the closing beauty state.

Emotion: presence. This is how it should work.

---

## HTML layer over the film (not generated)

| Leg | Words on screen |
|---|---|
| 1 | SmartScout wordmark only |
| 2 | The question. |
| 3 | The search. |
| 4 | Three names. |
| 5 | Signed. |
| 6 | (nothing; the flight breathes) |
| 7 | Find them before anyone else does. + Request a demo |
