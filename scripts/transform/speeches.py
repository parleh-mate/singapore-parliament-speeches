from bs4 import BeautifulSoup
import pandas as pd
import transform
import re
import nltk
from nltk.corpus import cmudict


def speech_cid(row):
    return f"{row['Topic_CID']}-S-{row['speech_order']:05}"


def clean_rows(temp_df):
    # 1. Remove HTML tags from header
    temp_df["Text"] = temp_df["Text"].apply(
        lambda x: BeautifulSoup(x, "html.parser").get_text()
    )

    # 2. Remove "proc text" from header
    temp_df["Text"] = temp_df["Text"].str.replace("proc text", "", case=False)

    # 3. Remove "pages" from header
    temp_df["Text"] = temp_df["Text"].str.replace(r"Page  \d+", "", regex=True)

    # 4. Remove "None" from header
    temp_df["Text"] = temp_df["Text"].str.replace("None", "")

    # 5. Drop blank rows
    temp_df = temp_df[temp_df["Text"].astype(str) != ""]

    return temp_df


def topic_dataframe(content, topic_cid, index):
    soup = BeautifulSoup(content, "html.parser")
    speakers, texts = process_content(soup)
    print(f"Topic: {topic_cid}, Index (of Topic List): {index}")

    cleaned_speakers = [transform.get_mp_name(speaker) for speaker in speakers]

    temp_df = pd.DataFrame(
        {
            "date": [topic_cid[:10]] * len(speakers),
            "Topic_CID": [topic_cid] * len(speakers),
            "Original_MP_Name": speakers,
            "MP_Name": cleaned_speakers,
            "Text": texts,
        }
    )

    if len(temp_df) > 0:
        temp_df = clean_rows(temp_df)

    return temp_df


def count_words_and_characters(row):
    text = row["Text"]
    words = text.split()
    num_words = len(words)
    num_characters = len(
        re.findall(r"[a-zA-Z]", text)
    )  # count only alphabetic characters

    return pd.Series({"num_words": num_words, "num_characters": num_characters})


def calc_number_of_sentences(text):
    # Split text into sentences
    sentences = re.split(r"[.!?]+", text)
    # Remove empty strings (e.g., caused by trailing punctuation)
    sentences = [sentence for sentence in sentences if sentence]
    return len(sentences)


def count_syllables(word):
    # Define vowels
    vowels = "aeiouy"
    # Convert word to lowercase
    word = word.lower()
    # Initialize syllable count
    count = 0
    # Initialize flag to track if previous character was a vowel
    prev_char_was_vowel = False

    # Iterate through each character in the word
    for char in word:
        # Check if the character is a vowel
        if char in vowels:
            # Check if the previous character was not a vowel
            if not prev_char_was_vowel:
                # Increment syllable count for a new vowel sequence
                count += 1
            # Update the flag
            prev_char_was_vowel = True
        else:
            # Update the flag if the character is not a vowel
            prev_char_was_vowel = False

    # Adjust syllable count for specific cases
    if word.endswith(("e", "es", "ed")) and not word.endswith(("le", "ble", "ple")):
        count -= 1
    # Ensure at least one syllable for any word
    if count == 0:
        count = 1

    # Return the calculated syllable count
    return count


def calc_number_of_syllables(text):
    """Calculate the number of syllables in a given text."""
    words = nltk.word_tokenize(text)
    syllable_counts = [count_syllables(word) for word in words]
    return sum(syllable_counts)


def process_content(soup):
    # 1. get content out

    speakers = []
    texts = []
    sequences = []

    for index, p in enumerate(soup.find_all("p")):
        try:
            if p.strong:
                if str(p.strong.text).strip() == "" and index > 0:
                    speaker = speakers[-1]
                else:
                    speaker = str(p.strong.text).strip()
                text = str(p.find("strong").next_sibling)
                if p.find("span"):  # In cases where there are 'span's in the text
                    text = text + " " + p.find("span").get_text()
                sequence = 1
            else:
                if len(speakers) > 0:
                    speaker = speakers[-1] if index > 0 else ""
                    sequence = sequences[-1] + 1 if index > 0 else 1
                else:
                    # where the question stood in the name of the member,
                    # the name is in the prior <p> tag
                    if soup.find_all("p")[index - 1].strong.text.strip():
                        speaker = soup.find_all("p")[index - 1].strong.text.strip()
                    else:
                        speaker = ""
                    sequence = 1
                text = str(p.text)

            speakers.append(speaker)
            texts.append(
                text.strip()
                .replace("\xa0", " ")
                .replace("\t", " ")
                .replace(":", " ")
                .strip()
            )
            sequences.append(sequence)
        except Exception as e:
            print(f"Error at: {index} - {e}")

    # 2. combine texts by speaker

    revised_speakers = []
    revised_texts = []

    last_speaker = None

    for index in range(len(speakers)):
        # other conditions are indicative of a question, and therefore should not be added to the next text
        if (
            last_speaker == speakers[index]
            and not texts[index].strip().lower().startswith("asked")
            and not "to ask" in texts[index].strip().lower()[:10]
        ):
            revised_texts[-1] += " " + texts[index]
        else:
            revised_speakers.append(speakers[index])
            revised_texts.append(texts[index])
            last_speaker = speakers[index]

    return revised_speakers, revised_texts
