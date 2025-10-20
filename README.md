# Last FM Collage Maker

**Last FM Collage Maker** is a software for generating album cover collages based on your recently listened albums from [last.fm](last.fm). The **main** feauture of this exact collage generator is that it [**finds missing album covers**](#search-for-missing-covers).

## Navigation

  - [Installation](#installation)
  - [Guidance on the use](#guidance-on-the-use)
  - [Settings](#settings)
    - [Main settings](#main-settings)
    - [Collage settings](#collage-settings)
  - [Search for missing covers feature](#search-for-missing-covers)

  
---

## Installation

### Do the following steps in your terminal

1. Clone this repository to any directory on your computer

    ```bash
    git clone https://github.com/samheartache/LastFM-collage-maker.git
    ```
2. Set up your virtual environment

    ### Windows:

    ```bash
    python -m venv .venv
    ```

    ```bash
    .venv\Scripts\activate
    ```

    ### Linux:

    ```bash
    python3 -m venv .venv
    ```

    ```bash
    source .venv/bin/activate
    ```
3. Install all dependencies
   ```
   pip install -r requirements.txt
   ```
4. Run the **main.py** script

    ### Windows:

   ```bash
    python main.py
    ```

    ### Linux

    ```bash
    python3 main.py
    ```

5. ### Only available on Linux now:
   
   You can run **install.sh** script and then you'll be able to launch the software from anywhere just by typing "**lastfm**" in your terminal instead of running main.py script everytime.
    #### Note: before doing it make sure that you named your virtual environment exactly "**.venv**"

    - ### Run the install.sh script

        ```bash
        bash install.sh
        ```
    - ### Launch the software

        ```bash
        lastfm
        ```    

## Guidance on the use

### Before using the software you should get your **Lastfm API key**. It is **FREE** and **everyone** can get it on [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)

### Here are the available functions from the main menu

```
[1] Make a collage of album covers
[2] Parse your albums to text file
[3] Download album covers (text file with titles is needed)
[4] Make a collage of already downloaded images
[5] Change/view main settings
[6] Delete images from a collage by the index number
[7] Change Last.fm API key
[8] Guidance on the use
[9] Stop the software
```

 All names of the albums are stored in **albums.txt**, unfortunately it happens that it is impossible to define the album for some songs, so the names of these songs are stored in **unknown.txt**

### Explanation on [6] function (Delete images from a collage by the index number)

By default there're two collages generating as a result, the collage of album covers itself and the collage with numerated covers to make it easier to delete them by order number. So you can always enter the right indexes of the covers to remove them from your collage. Also you can just disable numerate collage generating in the collage settings.

## Settings

All of the settings are divided into two categories: **main settings** and **collage settings**

### Main settings

- **Username** - username of your [last.fm](last.fm) account
- **Time** - time from which albums will be selected
    #### You can set time to "week", "month" or any number of days (for exaple 10, 14, 60)


- **Delay** - number of seconds to stop for when downloading album covers that are not on [last.fm](last.fm), to avoid bot detection. (the delay is implementing **only when searching for [missing covers](#search-for-missing-covers)**)
  
  The default 2 seconds setting can handle downloading a lot of images, but if you going to make for exaple "month" collage or any collage that contains a lot of covers, it is better for you to set this to at least 5 seconds.
- **Timeout** - maximum time of waiting the response from [last.fm](last.fm) to download album cover. 
- **Default collage directory** - directory where all your collages are stored.

  By default it is just "Collages" so every collage will be saved in this directory. If it doesn't exist in the directory from where the software was launched it will be created. So you can just specify any other absolute path instead of it.
- **Auto name image directory or collage file** - you can either set this to any name you want or just set this to true/false. If true the certain directory or file will be named with the date and time of creation the collage. If false you'l be asked how to name file/directory.
- **Image direcrory or collage file suffix** - string that will be added to the name of your file/directory if it is autonamed with the date and time of creation.
- **Delete omitted images** - possible options: true, false. Defines the need of deleting the images that was removed from the collage by their index. (false is recommended)
- **Directory for the omitted images** - directory that will be created (if doesn't exist) for album covers that was removed from the collage by their index.
  
    If you accidentally removed some cover from the collage, you can just move it to directory where all of the covers are stored and recreate the collage.
- **Logo** - possible options: 0, 1. 0 for small logo and 1 for big logo.
  
    To make sure that logo will fit in your terminal leave the default 0 setting.


### Collage settings
- **Collage size** - approximate size of the collage in pixels.
The final dimensions will be close to this value but may vary depending on the number of covers and their arrangement.
- **Margin** - margin in pixels between images
- **Create numerate collage** - possible options: true, false. Defines the need of generating the collage with numbered covers.
- **Scale center** (true recommended):
   - **True**  - prevents image distortion by scaling to the center of it
   - **False** - showing the entire image content, but may cause image distortion by stretching it

- **Ask about changing the collage** - possible options: true, false. If true, you'll be asked about the need of deleting certain images from your collage after it'll be generated.

## Search for missing covers

Sometimes [last.fm](last.fm) doesn't have covers for rare albums, demos or another types of releases. So this collage generator provides feature for finding them.

### How It Works
- **Detection**: Identifies albums without covers in your Last.fm data
- **Search**: Performs automated Google Images search using album titles
- **Download**: Retrieves the first cover that pops up as a result of the search

### Technology
  Uses python **Selenium** framework for automatic search. It implements the search of queries really rapidly, that's why it is recommended to use "**Delay**" settings value to avoid bot detection. Of course you can set this setting to 0 seconds, but then it is not guaranteed that all of your album covers will be downloaded, especially when there're a lot of them.

### Perfect For
- Rare and hard-to-find releases
- Local/underground music scenes  
- Demo tapes
  
### Note: 
When your cover is downloaded its title will be displayed in the terminal as a log information like this:

    <album title> (<download method>)

Where download method can be either "**url**" or "**selenium**".
  - "**url**" - downloaded directly from [last.fm](last.fm)
  - "**selenium**" - downloaded using automatic google image search