def createSeminar(title, capacity, timeStart, timeEnd, lastTimeToLeave,
                        desc, fee, earlyBirdTime, sessionCount, sessions):
    buf = {
        'title':title,
        'capacity':capacity,
        'timeStart':timeStart,
        'timeEnd':timeEnd,
        'lastTimeToLeave':lastTimeToLeave, 
        'description':desc,
        'fee':fee,
        'earlyBirdTime': earlyBirdTime,
        'sessionCount': sessionCount,
        **sessions
    }

    return buf

def createSession(title, timeStart, timeEnd, desc, presenter, capacity, i):
    form = {
        ('session{}_title'.format(i)):title,
        ('session{}_timeStart'.format(i)):timeStart,
        ('session{}_timeEnd'.format(i)):timeEnd,
        ('session{}_description'.format(i)):desc,
        ('session{}_presenter'.format(i)):presenter,
        ('session{}_capacity'.format(i)):capacity
        }
    return form

class Sample_Seminars():

    def __init__(self):        
        session1_0 = createSession(
            "History of Microsoft Word",
            "2018-06-15T06:00",
            "2018-06-15T08:00",
            "How back in the days Notepad was the way to go for everything.",
            "catchermuted@gmail.com",
            "5000",
            0
        )
       
        session1_1 = createSession(
            "Introduction to the fonts",
            "2018-06-18T06:00",
            "2018-06-18T08:00",
            "Times new Roman, Arian, Georgia and WORDART",
            "catchermuted@gmail.com",
            "5000",
            1
        )
        
        session1_2 = createSession(
            "Data structures of Microsoft Word: pictures, shapes and footers",
            "2018-06-21T06:00",
            "2018-06-21T08:00",
            "Very useful if you want to impress the millenials",
            "catchermuted@gmail.com",
            "500",
            2
        )
        
        session1_3 = createSession(
            "Mastering QWERTY",
            "2018-06-24T06:00",
            "2018-06-24T08:00",
            "Very useful if you grew up in Germany and are used to typing via QWERTZ",
            "hatsobey@gmail.com",
            "50",
            3
        )
        
        session1_4 = createSession(
            "Challendge: Introduction to Visual Basic",
            "2018-06-27T06:00",
            "2018-06-27T12:00",
            "And discover how much the short-circuit logical statements in C are the masterpiece",
            "catchermuted@gmail.com",
            "10",
            4
        )
        
        seminar1 = createSeminar(
            "Mastering Microsoft Word",
            "5000",
            "2018-06-15T06:00",
            "2018-07-15T06:00",
            "2018-07-14T08:00",
            "Ever wanted to master computers? Perhaps discover some amazing fonts and Wordart? Then this seminar is for you.",
            "200",
            "2018-05-15T06:00",
            "5",
            {**session1_0, **session1_1, **session1_2, **session1_3, **session1_4}
        )
        
        session2_0 = createSession(
            "Beginner",
            "2018-08-15T06:00",
            "2018-08-15T07:00",
            "Learn the meanings of the numbers on the screen",
            "informalfrontal@gmail.com",
            "100",
            0
        )
        
        session2_1 = createSession(
            "Intermediate",
            "2018-08-24T06:00",
            "2018-08-24T09:00",
            "Corner numbers, shortcuts and basic implications",
            "informalfrontal@gmail.com",
            "100",
            1
        )
        
        session2_2 = createSession(
            "Professional",
            "2018-08-28T06:00",
            "2018-08-28T16:00",
            "Discover the secrets of the bad outcome probability's statistical analysis in the desperate situations; and complex implication analysis.",
            "informalfrontal@gmail.com",
            "100",
            2
        )
        
        seminar2 = createSeminar(
            "Minesweeper: A complete guide",
            "5000",
            "2018-07-15T06:00",
            "2018-08-15T06:00",
            "2018-05-31T08:00",
            "Validate yourselves in the modern society: stretch your brain and learn to play Minesweeper. ",
            "50",
            "2018-05-15T06:00",
            "3",
            {**session2_0, **session2_1, **session2_2}
        )
        
        session3_0 = createSession(
            "Cybercrimes",
            "2018-07-02T06:00",
            "2018-07-02T09:00",
            "Julian Assange, NSA, WikiLeaks and illegal services online.",
            "momentfunctional@gmail.com",
            "300",
            0
        )
        
        session3_1 = createSession(
            "It is not me, it is my frontal lobe",
            "2018-05-13T06:00",
            "2018-05-13T09:00",
            "How much the bad behaviour is hardcoded into our brains",
            "momentfunctional@gmail.com",
            "300",
            1
        )
        
        session3_2 = createSession(
            "Tendencies",
            "2018-05-16T06:00",
            "2018-05-16T09:00",
            "Why some suburbs are so criminalised",
            "kafire@gmail.com",
            "300",
            2
        )
        
        session3_3 = createSession(
            "Evolvement of traditional crime",
            "2018-05-20T06:00",
            "2018-05-20T09:00",
            "Why don't criminals steal VCRs any longer",
            "draughtpedals@gmail.com",
            "300",
            3
        )
        
        session3_4 = createSession(
            "Juvenile criminals",
            "2018-05-27T06:00",
            "2018-05-27T09:00",
            "Are the biggest users of public spaces indeed take made big contributions o the crime?",
            "catchermuted@gmail.com",
            "300",
            4
        )
        
        session3_5 = createSession(
            "Organised crime",
            "2018-06-04T06:00",
            "2018-06-04T09:00",
            "Italian maffia, Drug cartels, persons smuggling and exploitation, Thai homemade firearms.",
            "cheeseyages@gmail.com",
            "300",
            5
        )

        session3_6 = createSession(
            "Crimes against humanity and Genocides",
            "2018-06-11T06:00",
            "2018-06-11T09:00",
            "ICTY, ICTR, Turkey, Slobodan Praljak and Responsibity to Protect",
            "gatoradekickin@gmail.com",
            "300",
            6
        )
        
        session3_7 = createSession(
            "Crimes in the seas",
            "2018-06-18T06:00",
            "2018-06-18T09:00",
            "All sorts of nasty things happening in the seas, covered by the flags of convenience.",
            "stellerburkitt@gmail.com",
            "300",
            7
        )
        
        session3_8 = createSession(
            "STEM",
            "2018-06-25T06:00",
            "2018-06-25T09:00",
            "Collaboration is the way-to-go",
            "stellerburkitt@gmail.com",
            "300",
            8
        )
        
        
        seminar3 = createSeminar(
            "Crime through the ages",
            "500",
            "2018-05-13T06:00",
            "2018-07-20T06:00",
            "2018-04-13T06:00",
            "Learn how criminology and criminals evolve",
            "100",
            "2018-04-13T06:00",
            "9",
            {
            **session3_0, 
            **session3_1, 
            **session3_2,
            **session3_3,
            **session3_4, 
            **session3_5, 
            **session3_6,
            **session3_7, 
            **session3_8
            }
        )
        self.seminars = [seminar1, seminar2, seminar3]
        

