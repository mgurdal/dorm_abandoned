import random
from datetime import datetime
from contextlib import ExitStack

# core
from database.drivers import Sqlite
from database import models
from config import DATABASES

quiz = [
    {
      "Question": "Who’s da jawn who directed films like To Catch a Thief, The 39 Steps, and Psycho are some of the films directed by him?",
      "Answers": [
        "Alfred Hitchcock",
        "Stanley Kubrick",
        "Woody Allen",
        "Martin Scorcese",
        "Tim Burton",
        "Wes Anderson",
        "Christopher Nolan",
        "Ridley Scott"
      ]
    },
    {
      "Question": "This online multiplayer jawn popped out in 2004 has like a hella of alot people playing it all over the place?",
      "Answers": [
        "World of Warcraft",
        "Star Wars: The Old Republic",
        "The Matrix Online",
        "City of Heroes",
        "DC Universe Online",
        "Silent Hill",
        "Eve Online",
        "Batman Arkham Asylum"
      ]
    },
    {
      "Question": "How H.A.A.M (Hot as a Mother)is lightning?",
      "Answers": [
        "30,000 degrees celsius",
        "400.1  degrees",
        "40,000 degrees celsius",
        "46,000 degrees",
        "18,000 degrees celsius",
        "a hell of a lot",
        "50,00 degrees celsius",
        "98 degrees"
      ]
    },
    {
      "Question": "Who was the Bae of Joe Dimaggio, Arthur Miller, and John F. Kennedy for a time?",
      "Answers": [
        "Marilyn Monroe",
        "Dorothy Arnold",
        "Jacqueline Kennedy",
        "Mary Grace Slatterly",
        "Beyonce",
        "Wes Anderson",
        "Oprah Winfrey",
        "Inge Morath"
      ]
    },
    {
      "Question": "Bill Clinton was caught cheating on his wifey in 1998, but who was the ratchet he shackled up wit?",
      "Answers": [
        "Monica Lewinsky",
        "Maria Chapur",
        "Nikki Haley",
        "Ruth Bader Ginsburg",
        "Lisa Simpson",
        "Courtney Love",
        "Condoleezza Rice",
        "Shaquille O'Neal"
      ]
    },
    {
      "Question": "What was the jawn that capped Abraham Lincoln?",
      "Answers": [
        "A .44-Caliber Pistol",
        "Knife",
        "Saber",
        "Axe",
        "Whip",
        "Arsenic",
        "Bruce Lee's Bare Hands",
        "House Fire"
      ]
    },
    {
      "Question": "Which of these Civil War bruh’s was wit-out a West Point degree?",
      "Answers": [
        "David Farragut",
        "Ulysses S. Grant",
        "George McClellon",
        "John Garland",
        "Albert Johnson",
        "John Wool",
        "David Petraeus",
        "Robert E. Lee"
      ]
    },
    {
      "Question": "What jawn of wooder did the first president cross to fight dem Hussians?",
      "Answers": [
        "Delaware",
        "Colorado",
        "Mississippi",
        "Schuylkill",
        "Newark Bay",
        "Tigris",
        "Euphrates",
        "Gulf of California"
      ]
    },
    {
      "Question": "What was the ish’ that caused Richard Nixon to declare deuces from his prez gig?",
      "Answers": [
        "Watergate",
        "Walter Reed",
        "Yellowcake",
        "Bridgegate",
        "Filegate",
        "Iraqgate",
        "Monicagate",
        "Pastagate"
      ]
    },
    {
      "Question": "What Hood did Barack Obama come from?",
      "Answers": [
        "Honolulu, Hawaii",
        "Auburn, Alabama",
        "Hamilton, New Jersey",
        "Austin, Texas",
        "Orlando, Florida",
        "Cairo, Egypt",
        "London, England",
        "Hightstown, New Jersey"
      ]
    },
    {
      "Question": "What was the name of the jawn in 1941 that made the country bug out and go to war with the world, AGAIN?",
      "Answers": [
        "Pearl Harbor",
        "Trail of Tears",
        "Marais des Cygnes massacre",
        "Boston Massacre",
        "Ludlow Massacre",
        "Cairo, Egypt",
        "Bisbee Massacre",
        "Battle of Verdun"
      ]
    },
    {
      "Question": "This jawn published in 1925 is internationally known as THE novel of The Lost Generation",
      "Answers": [
        "The Great Gatsby",
        "To Kill a Mockingbird",
        "The Hunger Games",
        "On The Road",
        "The Sun Also Rises",
        "The Sound and The Fury",
        "Wuthering Heights",
        "The Yellow Wallpaper"
      ]
    },
    {
      "Question": "This chick, known for her fresh 3-D pieces were she  paints on all kinds of jawns like people, never studied art in college but did it all on her own.",
      "Answers": [
        "Alexa Meade",
        "Darsh Snow",
        "Greg Simkins",
        "Rosy Lamb",
        "Lady Gaga",
        "Vincent Van Gogh",
        "Brian Michael Reed",
        "Margaret Boozer"
      ]
    },
    {
      "Question": "This fool is Snoop Dogg’s/Lion’s cousin, known for getting turnt up Happy and his giant dope brown hat.",
      "Answers": [
        "Pharrell Williams",
        "Madonna",
        "Will Ferrell",
        "Akon",
        "Eminem",
        "Rain",
        "Psy",
        "Taylor Swift"
      ]
    },
    {
      "Question": "This fool wrote about Trees and Roads and stuff. One of his rhymes was: “and she loved the boy very very much, even more than she loved herself.",
      "Answers": [
        "Shel Silverstein",
        "Maya Angelou",
        "Tupac",
        "BJ Ward",
        "David Unger",
        "Michelle Tea",
        "Kim Stafford",
        "Phillip Schultz"
      ]
    },
    {
      "Question": "This Philly brah (EAGLES!) popped out Monopoly and other board jawn.",
      "Answers": [
        "Charles Darrow",
        "Ayn Rand",
        "Klaus Teuber",
        "Rick Priestley",
        "Gus Savage",
        "Oprah Winfrey",
        "Bart Simpson",
        "Reuben Klamer"
      ]
    },
    {
      "Question": "What was the name of that green dinosaur jawn who was killem wit that little plumber dude Mario on his back?",
      "Answers": [
        "Yoshi",
        "Wario",
        "Luigi",
        "Super Bowser",
        "Princess Peach",
        "Blue Falcon",
        "Toad",
        "Link"
      ]
    },
    {
      "Question": "If the first jawn is 0, 1, 1, 2, then the next ish of numbers is 3, 5, 8, 13, 21,  then what comes out after 34?",
      "Answers": [
        "21",
        "23",
        "27",
        "30",
        "6",
        "A1",
        "90",
        "22"
      ]
    },
    {
      "Question": "Little Boy and Fatman were code-names for what piece?",
      "Answers": [
        "The Atomic Bomb",
        "The 240 Bravo Machine Gun",
        "The M-4 rifle",
        "44 Magnum",
        "RPG-7",
        "M1 Abrams Tank",
        "MIM 104 PATRIOT",
        "Nike Ajax"
      ]
    },
    {
      "Question": "When did that first fresh iPod come out looking all legit?",
      "Answers": [
        "2001",
        "2002",
        "1999",
        "2000",
        "1971",
        "1989",
        "1998",
        "1991"
      ]
    }
]

quiz_2 = [
{
"question": "What is the scientific name of a butterfly?",
"answers": [
"Apis",
"Coleoptera",
"Formicidae",
"Rhopalocera"
],
"correctIndex": 3
},
{
"question": "How hot is the surface of the sun?",
"answers": [
"1,233 K",
"5,778 K",
"12,130 K",
"101,300 K"
],
"correctIndex": 1
},
{
"question": "Who are the actors in The Internship?",
"answers": [
"Ben Stiller, Jonah Hill",
"Courteney Cox, Matt LeBlanc",
"Kaley Cuoco, Jim Parsons",
"Vince Vaughn, Owen Wilson"
],
"correctIndex": 3
},
{
"question": "What is the capital of Spain?",
"answers": [
"Berlin",
"Buenos Aires",
"Madrid",
"San Juan"
],
"correctIndex": 2
},
{
"question": "What are the school colors of the University of Texas at Austin?",
"answers": [
"Black, Red",
"Blue, Orange",
"White, Burnt Orange",
"White, Old gold, Gold"
],
"correctIndex": 2
},
{
"question": "What is 70 degrees Fahrenheit in Celsius?",
"answers": [
"18.8889",
"20",
"21.1111",
"158"
],
"correctIndex": 2
},
{
"question": "When was Mahatma Gandhi born?",
"answers": [
"October 2, 1869",
"December 15, 1872",
"July 18, 1918",
"January 15, 1929"
],
"correctIndex": 0
},
{
"question": "How far is the moon from Earth?",
"answers": [
"7,918 miles (12,742 km)",
"86,881 miles (139,822 km)",
"238,400 miles (384,400 km)",
"35,980,000 miles (57,910,000 km)"
],
"correctIndex": 2
},
{
"question": "What is 65 times 52?",
"answers": [
"117",
"3120",
"3380",
"3520"
],
"correctIndex": 2
},
{
"question": "How tall is Mount Everest?",
"answers": [
"6,683 ft (2,037 m)",
"7,918 ft (2,413 m)",
"19,341 ft (5,895 m)",
"29,029 ft (8,847 m)"
],
"correctIndex": 3
},
{
"question": "When did The Avengers come out?",
"answers": [
"May 2, 2008",
"May 4, 2012",
"May 3, 2013",
"April 4, 2014"
],
"correctIndex": 1
},
{
"question": "What is 48,879 in hexidecimal?",
"answers": [
"0x18C1",
"0xBEEF",
"0xDEAD",
"0x12D591"
],
"correctIndex": 1
}
]
class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

if __name__ == '__main__':
    with ExitStack() as stack:
        dbs = [stack.enter_context(Sqlite('datastore/poll_1001.db')) for db in DATABASES[:1]]
        for db in dbs:
            try:
                db.create_table(Question)
                db.create_table(Choice)
            except:
                pass

        for data in quiz_2:
            
            question = Question(question_text=data["question"], pub_date=datetime.now())
            question.save()

            for answer in data["answers"]:
                choice = Choice(question=question, choice_text=answer, votes=random.randint(3, 15))
                choice.save()