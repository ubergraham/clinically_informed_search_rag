# terminal command to run: python clinical_note_generator.py

import anthropic
import os

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="ANTHROPIC API KEY",
)

topics = [
    {"type": "admission", "topic": "Hospital admission H&P for patient with pneumonia"},
    {"type": "admission",
        "topic": "Hospital admission H&P for patient with acute appendicitis"},
    {"type": "admission", "topic": "Hospital admission H&P for patient with COPD exacerbation"},
    {"type": "discharge",
        "topic": "Hospital discharge summary for patient with acute myocardial infarction"},
    {"type": "discharge", "topic": "Hospital discharge summary for patient with lower GI bleeding status-post colonoscopy"},
    {"type": "discharge", "topic": "Hospital discharge summary for patient with more lower GI bleeding status-post colonoscopy"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for a routine checkup in January"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for a routine checkup in March "},
    {"type": "progress",
        "topic": "Clinic progress note for patient for a routine checkup in August"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for a routine checkup in October"},
    {"type": "progress", "topic": "Clinic progress note for patient for an itchy rash"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for a cholesterol screening"},
    {"type": "progress", "topic": "Clinic progress note for patient for preventative health checkup indicating he is due for a colonscopy"},
    {"type": "progress", "topic": "Clinic progress note for patient for chronic knee pain"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for dizziness"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for fatigue"},
    {"type": "progress",
        "topic": "Clinic progress note for patient for headaches"},
    {"type": "progress", "topic": "Clinic progress note for patient for low blood sugars in the morning"}
    {"type": "procedure",
        "topic": "Long operative note for patient with routine uncomplicated appendectomy"},
    {"type": "procedure", "topic": "Complete procedure note for patient on eliquis for diagnostic colonoscopy for GI bleeding found to have severe diverticulosis "}
]

for item in topics:
    note_type = item["type"]
    topic = item["topic"]

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=3000,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Acting as a thorough senior medical resident, you should create notes about patient Steven Chou, aged 65, DOB Jan 7, 1959. He has a past medical history of diabetes, atrial fibrillation, high blood pressure, hypertension, and cholecystectomy. He takes eliquis, lisinopril, aspirin, plavix, metoprolol, and simvastatin. The note you should create is: {topic}."
                    }
                ]
            }
        ]
    )

    # Create the folder if it doesn't exist
    if not os.path.exists(note_type):
        os.makedirs(note_type)

    # Generate the file name based on the topic
    file_name = topic.lower().replace(" ", "_") + ".txt"

    # Write the generated content to a new text file in the corresponding folder
    with open(os.path.join(note_type, file_name), "w") as file:
        file.write(message.content[0].text)

    print(f"Generated {file_name} in {note_type} folder")
