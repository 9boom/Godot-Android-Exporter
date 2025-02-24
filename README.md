# Godot Android Exporter

For converting a Godot project into an Android APK installer file for those using the mobile version of the Godot Editor.

## ⚙️ System Requirements

- 📱 **Termux**: A Linux environment for Android ([Download from F-Droid](https://f-droid.org/repo/com.termux_118.apk))
    
- 📦 Install basic packages in Termux:
    
    ```
    pkg update -y && pkg upgrade -y
    ```
    
- 📦 Install **git**:
    
    ```
    pkg install git
    ```
    

## 🚀 Installation

1. Clone the repository:
    

```
git clone https://github.com/9boom/Godot-Android-Exporter
```

2. Navigate to the project directory:
    

```
cd Godot-Android-Exporter
```

1. Grant permission for the setup script:
    

```
chmod +x setup.sh
```

2. Run the setup script to install required dependencies:
    

```
./setup.sh
```

3. If installation is successful, you should see output similar to the following:
    

![Alt Text](https://raw.githubusercontent.com/9boom/Godot-Android-Exporter/main/screenshots/Screenshot_20250223-115612.png)

---

## 📝 Usage

### 📤 Exporting the Project from Godot

4. Open your project in **Godot Editor**.
    
5. Navigate to **Project > Export...**.
    
6. Select **Android (APK)** and click **Export Project**.
    
7. Set the file type to **Zip File**, then rename it to **assets.zip**.
    
8. Choose a save location and click **Save**.
    

![Alt Text](https://raw.githubusercontent.com/9boom/Godot-Android-Exporter/main/screenshots/Screenshot_20250223-142618_1.png) 
![Alt Text](https://raw.githubusercontent.com/9boom/Godot-Android-Exporter/main/screenshots/Screenshot_20250223-142809_2.png)

9. Edit **properties.gae** in **Godot-Android-Exporter** to configure your app settings.
    
    - You must set the `project_zip_file` variable to the path of your `assets.zip` file.
        
    - Other variables will use default values if not modified.
        

![Alt Text](https://raw.githubusercontent.com/9boom/Godot-Android-Exporter/main/screenshots/Screenshot_20250223-151252.png)

10. Run the following command to generate the APK:
    

```
python3 gae10.py
```

11. Wait for the process to complete. Once finished, you will find the output file in the same directory as **Godot-Android-Exporter**.
    

![Alt Text](https://raw.githubusercontent.com/9boom/Godot-Android-Exporter/main/screenshots/Screenshot_20250223-152710.png)

---

## 🛠️ Step-by-Step Guide for Beginners

If you are new to Linux commands, follow these detailed steps to ensure a smooth installation and usage experience.

### 1️⃣ Install and Setup Termux

1. Download and install [Termux](https://f-droid.org/repo/com.termux_118.apk) from F-Droid.
    
2. Open Termux and update the package list by typing:
    
    ```
    pkg update && pkg upgrade -y
    ```

   - If while running it asks you something like this. Just press **'Y'** and enter
    ```bash
    'Configuration file /data/data/com.termux/files/usr/etc/tls/openssl.cnf'
     ==> File on system created by you or by a script.
     ==> File also in package provided by package maintainer.
   What would you like to do about it ?  Your options are:
    Y or I  : install the package maintainer's version
    N or O  : keep your currently-installed version
      D     : show the differences between the versions
      Z     : start a shell to examine the situation
    The default action is to keep your current version.
    *** openssl.cnf (Y/I/N/O/D/Z) [default=N] ?
    ```
    
3. Install `git` to download the required files:
    
    ```
    pkg install git
    ```
    

### 2️⃣ Download the Exporter Tool

1. Clone the repository (copy the tool’s files to your system):
    
    ```
    git clone https://github.com/9boom/Godot-Android-Exporter
    ```
    
2. Change the directory to the downloaded folder:
    
    ```
    cd Godot-Android-Exporter
    ```
    

### 3️⃣ Grant Permissions and Install Dependencies

1. Allow the setup script to run:
    
    ```
    chmod +x setup.sh
    ```
    
2. Execute the script to install necessary dependencies:
    
    ```
    ./setup.sh
    ```
    

### 4️⃣ Export and Convert Your Godot Project

1. Open **Godot Editor** on your phone.
    
2. Export the project as a **Zip File** (`assets.zip`).
    
3. Locate and note the saved file path.
    
4. Open Termux and navigate back to the exporter directory:
    
    ```
    cd Godot-Android-Exporter
    ```
    
5. Open the **properties.gae** file using a text editor like nano:
    
    ```
    nano properties.gae
    ```
    
    - Find the `project_zip_file` setting and update it to match your **assets.zip** file path.
        
    - Press **CTRL + X**, then **Y**, then **Enter** to save and exit.
        
6. Run the APK generator:
    
    ```
    python3 gae10.py
    ```
    
7. Wait until the APK is successfully built. The final APK file will be available in the same directory.
     
8. Move your APK to External Storage :
    
    ```
    cp your_app_name.apk /storage/emulated/0/Download
    ```

---

## ☕ Support the Developer

If you like this project, consider buying me a coffee! 😊

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/9boom)

## 📜 License

```
MIT License

Copyright (c) 2025 Pongsakorn Sriwichai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights                                          to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE                                           AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
