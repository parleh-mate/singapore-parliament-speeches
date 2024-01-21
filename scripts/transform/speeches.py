from bs4 import BeautifulSoup
import pandas as pd
import transform


def speech_cid(row):
    return f"{row['Topic_CID']}-S-{row['speech_order']:05}"


def topic_dataframe(content, topic_cid, index):
    soup = BeautifulSoup(content, "html.parser")
    speakers, texts, sequences = process_content(soup)
    print(f"Topic: {topic_cid}, Index (of Topic List): {index}")

    cleaned_speakers = [transform.get_mp_name(speaker) for speaker in speakers]

    temp_df = pd.DataFrame(
        {
            "Topic_CID": [topic_cid] * len(speakers),
            "Original_MP_Name": speakers,
            "MP_Name": cleaned_speakers,
            "Text": texts,
            "Seq": sequences,
        }
    )

    return temp_df


def process_content(soup):
    speakers = []
    texts = []
    sequences = []

    for index, p in enumerate(soup.find_all("p")):
        try:
            if p.strong:
                speaker = str(p.strong.text).strip()
                text = str(p.find("strong").next_sibling)
                if p.find("span"):  # In cases where there are 'span's in the text
                    text = text + " " + p.find("span").get_text()
                sequence = 1
            else:
                speaker = speakers[-1] if index > 0 else ""
                text = str(p.text)
                sequence = sequences[-1] + 1 if index > 0 else 1

            if text != "None":
                speakers.append(speaker)
                texts.append(
                    text.strip().replace("\xa0", " ").replace(":", " ").strip()
                )
                sequences.append(sequence)
        except:
            print("Error at: {index}")

    return speakers, texts, sequences
