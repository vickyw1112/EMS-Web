def createEvent(title, capacity, timeStart, timeEnd, lastTimeToLeave,
                    desc, fee, earlyBirdTime ):
    buf = {
        'title':title,
        'capacity':capacity,
        'timeStart':timeStart,
        'timeEnd':timeEnd,
        'lastTimeToLeave':lastTimeToLeave, 
        'description':desc,
        'fee':fee,
        'earlyBirdTime': earlyBirdTime
    }
    return buf

class Sample_Events():

    def __init__(self):
        e1 = createEvent(
            "2018 Mitsubishi Sustainability Lecture: The Promise and Peril of the Fourth Industrial Revolution",
            "900",
            "2018-05-30T17:30",
            "2018-05-30T21:00",
            "2018-05-30T18:30",
            "The lecture will explore how we might realise the benefits of sustainable, responsible and human-centred innovation.",
            "40",
            "2018-05-27T17:30"
        )


        e2 = createEvent(
            "Lethal Autonomous Robots and the plight of the non-combatant",
            "50",
            "2018-05-30T18:00",
            "2018-05-30T19:15",
            "2018-05-30T18:05",
            "Roboticist and robot ethics expert Ron Arkin asks if robots should be soldiers?",
            "20",
            "2018-05-30T12:00"
        )


        e3 = createEvent(
            "Hacky Hour with special guest Dr Jack Yang",
            "40",
            "2018-05-31T15:00",
            "2018-05-31T16:00",
            "2018-05-31T15:30",
            "Hacky Hour with a special talk on Accelerating Material Discovery with Artificial Intelligence by Dr Jack Yang.",
            "5000",
            "2018-04-31T15:00"
        )

        e4 = createEvent(
            "How do we know what our students know? The benefits of a hurdle-based approach to learning and assessment",
            "500",
            "2018-05-31T17:00",
            "2018-05-31T18:30",
            "2018-05-31T17:05",
            "There’s a problem with the way we assess our students. We don’t know what they know...",
            "8",
            "2018-05-30T17:00"
        )


        e5 = createEvent(
            "Software Carpentry (Intro to Unix, Python and Git)",
            "800",
            "2018-06-04T09:30",
            "2018-06-15T09:30",
            "2018-06-04T09:50",
            "Join us for this live two-day coding workshop where we write programs that produce results, using the researcher-focused training modules from the highly regarded Software Carpentry Foundation.",
            "40",
            "2018-05-31T17:00"
        )


        e6 = createEvent(
            "Reforming Australia's refugee policy: Where do we begin?",
            "2000",
            "2018-06-06T16:00",
            "2018-06-06T17:00",
            "2018-06-06T16:45",
            "Please join us for this Grand Challenge meetup, with guest speaker Paul Power, CEO of the Refugee Council of Australia.",
            "90000",
            "2018-06-06T11:00"
        )


        e7 = createEvent(
            "myExperience Dashboard: What's all the hype about?",
            "50",
            "2018-06-13T13:00",
            "2018-06-13T14:00",
            "2018-06-13T13:05",
            "We will explain in more detail how the myExperience program is carried out and discuss how it is affecting QA/QE processes.",
            "10",
            "2018-06-10T13:00"
        )
        self.events = [e1, e2, e3, e4, e5, e6, e7]

