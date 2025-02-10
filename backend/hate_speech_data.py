# hate_speech_data.py

HARD_CODED_HATE_ENGLISH = [
    "hate you", "you are stupid", "go to hell", "kill yourself", 
    "you are worthless", "nobody likes you", "you are disgusting",
    "die in a fire", "ugly piece of trash", "I wish you were dead",
    "you're a loser", "you suck", "shut up", "you're pathetic",
    "dumb", "moron", "idiot", "loser"
]

HARD_CODED_HATE_HINDI = [
    "तू बेवकूफ है", "तू मर जा", "तू कुछ नहीं है", "कुत्ते की औलाद", 
    "हरामी", "गंवार", "तेरी औकात नहीं", "निकल यहाँ से", "तू सड़ा हुआ है", 
    "तू कमीना है", "तेरी मम्मी", "साले", "गधे", "तू बेकार है", 
    "मर", "पागल", "तुच्छ"
]

HARD_CODED_HATE_MARATHI = [
    "तू मूर्ख आहेस", "तू मेलास पाहिजे", "तुझी किंमत काहीच नाही", 
    "हरामखोर", "गंवार", "तू निरुपयोगी आहेस", "निघ इथून", 
    "तुझी औकात नाही", "तू कुत्र्याचा पिल्लू आहेस", "मूर्ख", 
    "पागल", "तु नालायक आहेस", "गाढव", "मायच्याल", "शून्य"
]

HARD_CODED_HATE_BANGLA = [
    "তুই একটা গাধা", "তোর কোনো মূল্য নেই", "তুই মর", 
    "তোকে কেউ পছন্দ করে না", "তুই অকর্মণ্য", "শালা", 
    "তুই একটা কুত্তার বাচ্চা", "তোকে মেরে ফেলবো", "তোর মা", 
    "পাগল", "অপদার্থ", "গরু", "তুই বেকার", "তুই শয়তান"
]

HARD_CODED_NON_HATE = [
    "not hate you", "you are great", "have a nice day", 
    "तू महान है", "आप खूप छान आहात", "तू चांगला आहेस", 
    "তুমি ভালো", "তুমি সুন্দর", "love you"
]

HARD_CODED_HATE = (
    HARD_CODED_HATE_ENGLISH +
    HARD_CODED_HATE_HINDI +
    HARD_CODED_HATE_MARATHI +
    HARD_CODED_HATE_BANGLA
)
