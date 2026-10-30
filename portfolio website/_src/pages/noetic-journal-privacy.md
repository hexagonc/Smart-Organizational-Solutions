---
title: Noetic Journal privacy policy
out: apps/noetic-journal/privacy.html
description: How Noetic Journal for Android handles your data. No accounts, notes stay on your device, and optional features send data only to services you choose.
---
# Noetic Journal privacy policy

**Effective October 26, 2026.** This policy covers the Noetic Journal Android app (`com.evolved.automata.app.noeticjournal`, including its testing builds), published on Google Play by **Andrew Baughns**, the developer. Questions go to [abaughns12@gmail.com](mailto:abaughns12@gmail.com).

## Summary

- Noetic Journal has **no user accounts**. You never sign up or sign in to use it.
- Your notes, journals, tasks, scripts and settings are **stored on your device**. The developer does not receive them.
- Some optional features send data to services **you choose and configure**, such as an AI provider, your own server, or your Dropbox account. Nothing is sent to those services unless you set them up.
- The app sends the developer **anonymous usage and crash data** through Google Firebase so problems can be found and fixed.
- The app has no ads, and your data is **never sold**.

## Data stored on your device

Everything you create in Noetic Journal is kept in the app's private storage on your phone. That includes notes, collections, workspaces, journal entries, tasks, scripts and macros, saved places and location reminders, chat history with AI models, AI model settings, API keys you enter, downloaded AI and speech models, and app preferences.

Other apps cannot read the app's private storage. The data is removed when you delete it in the app, clear the app's storage in Android settings, or uninstall the app.

Photos you take with the in-app camera are saved to your device's shared `Pictures/NoeticJournal` folder, so they stay in your gallery even if you uninstall the app.

## Data the developer receives

### Usage analytics (Google Analytics for Firebase)

The app records which screens you open, for example "Library" or "Search". Firebase adds standard information: an app-instance identifier, device model, Android version, app version, and approximate country or region derived from your IP address. It does **not** include the content of your notes, chats, searches or files. The developer uses it only to understand which features are used. See [Google's privacy policy](https://policies.google.com/privacy) and [Firebase privacy and security](https://firebase.google.com/support/privacy).

### Crash reports (Firebase Crashlytics)

If the app crashes, Crashlytics sends a report with the stack trace, installation identifiers, the time of the crash, app version, Android version, device model, and memory and disk details. Crashlytics keeps this data for 90 days, according to [Firebase](https://firebase.google.com/support/privacy). Crash reports do not include your notes.

### On-device model downloads (Amazon Web Services)

When you download an on-device AI model from **Profile → Model configuration**, the app fetches the file from the developer's Amazon S3 storage. It uses anonymous, temporary AWS Cognito guest credentials, so no account is created. As with any download, AWS receives your IP address and the request details. See the [AWS privacy notice](https://aws.amazon.com/privacy/).

## Optional features that send data to services you choose

These features only send data after you turn them on or start the action yourself.

| Feature | What is sent | Where it goes |
|---|---|---|
| Cloud AI models | Your chat messages, the note or document text you include, and images when **Include images** is on | The provider you configure with your own API key, such as [OpenAI](https://openai.com/policies/privacy-policy), [Anthropic](https://www.anthropic.com/legal/privacy), [Google Gemini](https://policies.google.com/privacy) or [Together AI](https://www.together.ai/privacy) |
| Self-hosted AI (for example Ollama) | The same as above | The server address you enter, such as a computer on your home network |
| Dropbox backup, sync and file picker | Journal files and notes you back up or sync. The app also reads the folders and files you browse or pick | Your own Dropbox account, after you link it. See [Dropbox's privacy policy](https://www.dropbox.com/privacy) |
| Place search for location reminders | The place name or category you search for, plus an approximate area around you to narrow results | OpenStreetMap services (Nominatim and the Overpass API). See the [OpenStreetMap Foundation privacy policy](https://osmfoundation.org/wiki/Privacy_Policy) |

Data you send to these services is handled under their own privacy policies. Your API keys are sent only to the provider they belong to.

## Permissions

| Permission | Why the app asks |
|---|---|
| Camera | Take photos from inside the app and attach them to notes |
| Photos, videos and audio (media access) | Pick images to attach to notes and play music or media you choose |
| Microphone | Voice commands and dictation. Speech recognition runs on your device |
| Location, including background location | Location reminders that fire when you arrive at or leave a saved place, even when the app is closed. Locations are checked on your device |
| Notifications | Task reminders, scheduled commands, and controls for media playback |
| Foreground services and wake lock | Keep long tasks running, such as model downloads, backups, voice input and music playback |
| Internet and network state | Optional cloud features, model downloads, and crash and usage reporting |

You can deny or revoke any permission in Android settings. Only the features that need it stop working.

## Security

Connections to cloud AI providers, Dropbox, AWS, OpenStreetMap and Firebase use HTTPS. Connections to a self-hosted server use the address and protocol you configure. If you use plain `http://` on your local network, that traffic is not encrypted.

## Keeping and deleting your data

Because there are no accounts, there is no account to delete. You control your data directly:

- Delete individual notes, collections or chats in the app.
- Clear all app data in **Android Settings → Apps → Noetic Journal → Storage → Clear storage**, or uninstall the app.
- Backups in your Dropbox stay there until you delete them from Dropbox.

To ask for deletion of analytics or crash data tied to your device, email [abaughns12@gmail.com](mailto:abaughns12@gmail.com).

## Children

Noetic Journal is not directed at children under 13, and the developer does not knowingly collect personal information from children.

## Changes to this policy

If this policy changes, the new version will be posted on this page with a new effective date.

## Contact

Andrew Baughns, developer of Noetic Journal. Email: [abaughns12@gmail.com](mailto:abaughns12@gmail.com)
