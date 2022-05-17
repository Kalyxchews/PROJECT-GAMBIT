import random
import os
import sys
import time


# Standard per-character text printing.
def talk(phrase):
    i = 0
    while i < len(phrase):
        print(phrase[i], end='')
        sys.stdout.flush()
        time.sleep(0.03)
        i += 1
    print()


# Asks for input, checks expected responses,
# either returns if correct, re-prompts the player if not.
def ask(responses, phrase):
    talk(phrase)
    reduct1 = input("\t")
    reduct2 = str(reduct1)
    answer = reduct2.lower()
    if responses == (''):
        while answer == '' or answer == ' ':
            if answer == '' or answer == ' ':
                talk("Didn't hear you, stranger!")
                talk(phrase)
                reduct1 = input("\t")
                reduct2 = str(reduct1)
                answer = reduct2.lower()
            else:
                break
        answer = answer.upper()
    else:
        while answer not in responses:
            talk("I don't recognize that answer.")
            talk(phrase)
            reduct1 = input("\t")
            reduct2 = str(reduct1)
            answer = reduct2.lower()
    print()
    return answer


# A stat created for a little bit of session personalization.
def magic():
    try:
        userName = os.getlogin()
        fun = len(userName) + random.randint(0, 6)
    except FileNotFoundError:
        fun = random.randint(0, 12)
    if fun > 18:
        fun == random.randint(0, 18)
    return fun


# Creates the narrator's name.
def nameGen(fun):
    part1 = []
    if fun == 1:
        part1 = 'st'
    elif fun == 2:
        part1 = 'nd'
    elif fun == 3:
        part1 = 'rd'
    else:
        part1 = 'th'
    funnyList1 = str(fun) + part1
    funnyList2 = ['Ceres', 'Pallas', 'Juno', 'Vesta', 'Chiron', 'Ophiuchus',
                  'Sol', 'Mercurius', 'Venus', 'Lua', 'Terra', 'Mars',
                  'Veil', 'Deimos', 'Sedna', 'Eris', 'Void', 'Europa',
                  'Phobos', 'Uranus', 'Neptune', 'Jupiter', 'Saturn', 'Pluto']
    narrator = " ".join([funnyList1, funnyList2[fun]])
    return narrator


# A mechanic unique to the default item.
def luckyDice(fate):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    fate = (dice1 + dice2)
    kismet = random.randint(0, 18)
    if kismet > 12:
        fate = 18
        talk(str(dice1) + " and " + str(dice2) +
             " which results in ")
        talk(str(fate) +
             "! ... How strange, you had one extra "
             "stone for a fleeting moment.")
        return fate
    else:
        talk(str(dice1) + " and " + str(dice2) +
             " which results in " + str(fate) + "!")
        return fate


# Checks your current items to see if you have what's being asked for.
def itemUse(fate, action, items):
    def failAction():
        talk(f"Ah, seems you don't have that!")

    if action == 0:
        if 'Lucky Dice' in items:
            results = luckyDice(fate)
            return results
        else:
            failAction()
    if action == 1:
        if 'Molten Adamant' in items:
            return True
        else:
            failAction()
    if action == 2:
        if 'Coral Wreath' in items:
            return True
        else:
            failAction()
    if action == 3:
        if 'Dirty Ampoule' in items:
            return True
        else:
            failAction()
    if action == 4:
        if 'Stellated Sash' in items:
            return True
        else:
            failAction()
    if action == 5:
        if 'Bifurcated Pupil' in items:
            return True
        else:
            failAction()
    if action == 6:
        if 'Cellular Atrophy' in items:
            return True
        else:
            failAction()


# A very bare-bones battle system.
# Literally just checks to see if you have the right item.
def enemyEncounter(environment, fun, fate, items, itemsBank, blows):
    enemyList = ('Zukurou', 'Gaulem', 'Leviathan',
                 'Malboro', 'Asura', 'Oxonumo', 'Melon Bread')
    currentEnemy = enemyList[environment]
    weakTo = itemsBank[environment + 1]
    if currentEnemy == 'Zukurou':
        weakTo = itemsBank[0]
    elif currentEnemy == 'Oxonumo':
        weakTo = itemsBank[1]
    elif currentEnemy == 'Melon Bread':
        weakTo = itemsBank[6]
    criticalDestroyText = ['Your Lucky Dice spark to life '
                           'and leap from your flourishing '
                           'throw like glimmering comets '
                           'across shredding the dark into dust.',
                           'Your Coral Wreath exudes ghostly '
                           'tides of seawater that lash in'
                           'terrifying arcs like writhing '
                           'razorblades.',
                           'You jam the Dirty Ampoule into '
                           'the beast with a grisly crack. '
                           'The poison takes faster than the '
                           'trauma.',
                           'The herculean Stellated Sash wraps '
                           'your arms with divine power '
                           'that demands impure tribute.',
                           'The very touch of your Cellular Atrophy '
                           'makes them crumble. '
                           'There are no openings when your whole '
                           'body is a curse.',
                           'The Molten Adamant wraps you in an '
                           'impenetrable wall of boiling '
                           'air, no infection can outlast this fever '
                           'temp.',
                           'The Bifurcated Eye causes them to warp '
                           'into an unnatural shape. '
                           'You don\'t want to know why this works.']
    if weakTo in items:
        talk(f"You sense you have the upper hand.")
        talk(f"{criticalDestroyText[environment]}")
        return 0
    else:
        talk("Bad move. You came unprepared.")
        if 'Lucky Dice' in items:
            talk("[LUCKY DICE]")
            talk("But...")
            talk("There's still a chance.\n")
            talk("Taking the Lucky Dice into your hands, "
                 "you cup them between your palms, "
                 "then blow for luck.")
            input("Press ENTER and hope for a 12 or higher.")
            results = itemUse(fate, 0, items)
            if results >= 12:
                talk(f"Nice save.")
                return 0
            elif results < 12 and results > 6:
                talk(f"Damn. Still a saving throw.")
                return 1
            else:
                talk(f"Ouch. That didn't go so well.")
                blows += 1
                return 1
        else:
            blows += 1
            return 1


# Everything in this section is an environment to explore.
def enterNexus(limit, name, narrator, context, environment,
               fun, fate, worldList, possible, doors, items,
               itemsBank, defeats, blows):
    environment = 0
    alive = 1
    quest = 1
    talk("A comforting nothingness breezes through "
         "the dark hollow of this vast error.")
    while quest == 1:
        talk("The wind whistles past the "
             "frames of the enigmatic doors that stand "
             "free from walls.")
        talk("There are three paths to take. LEFT, "
             "FORWARD, and RIGHT. You can also just RUN.")
        answer = ask(('left', 'right', 'forward',
                      'run'), f"Where will you go?\n")
        if answer == 'left':
            talk("You turn to face the two left doors.")
            talk("There's a tingling at the back of your "
                 "neck.")
            talk("You can't remember why you're here.")
            talk("There are two paths to take. LEFT or "
                 "RIGHT. You can also just RUN.")
            answer1 = ask(('left', 'right', 'run'),
                          "Where will you go?")
            if answer1 == 'left':
                talk("Peering behind the leftmost door, "
                     "you sense something might have been "
                     "here previously.")
                talk("The Lucky Dice seem to shiver in "
                     "your pocket.")
                talk("You definitely feel lucky.\t")
                talk("\t[Your devilish charm heals you by 1.]\t")
                blows -= 1
            elif answer1 == 'right':
                talk("Peering behind the door slightly to "
                     "the left, you sense an ominous pair "
                     "of eyes.")
                talk("The Nexus has many things in it. You "
                     "have a brief double-take, and it is "
                     "no longer there.")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'forward':
            talk("You move into the center of the Nexus.")
            talk("Something about being surrounded by "
                 "the doors makes you feel dizzy.")
            talk("There are three paths to take. LEFT, "
                 "FORWARD, and RIGHT, where will you go?")
            answer2 = ask(('left', 'right', 'forward',
                          'run'), f"Enter LEFT, FORWARD, "
                          "RIGHT, or RUN.\n")
            if answer2 == 'left':
                talk("You check behind the middle-left "
                     "door.")
                talk("A strange voice speaks, but you "
                     "can't understand it.")
                talk("You try to listen more closely, "
                     "but now there is only silence.")
            elif answer2 == 'forward':
                talk("You stand in front of the two "
                     "middle doors and look forward.")
                if alive == 1:
                    talk("There is only void out there. "
                         "Do you want to try to explore "
                         "it anyway?")
                    answer2 = ask(('forward', 'run'),
                                  "Enter FORWARD, or "
                                  "RUN.\n")
                    if answer2 == 'forward':
                        talk("You run as far as your legs "
                             "can take you.")
                        talk("You no longer see the doors. "
                             "Just a swirling black "
                             "infinity in all directions.")
                        talk("You stare long into the "
                             "black. Perhaps your mind "
                             "deceives you, but the corners "
                             "of your vision begin to fold "
                             "inward.")
                        talk("Great wings stretching beyond "
                             "the horizon, beyond what is "
                             "possible, reveal themselves.\n")
                        talk("\tZukurou is upon you.\n")
                        alive = enemyEncounter(environment, fun,
                                               fate, items, itemsBank,
                                               blows)
                        if alive == 0:
                            defeats += 1
                            talk("You have defeated a "
                                 "tremendous threat.\n")
                            progressCheck(limit, name, narrator,
                                          context, environment, fun,
                                          fate, worldList, possible,
                                          doors, items, itemsBank,
                                          defeats, blows)
                        else:
                            blows += 1
                            if blows < 6:
                                talk("You escape with your "
                                     "life.\n")
                            progressCheck(limit, name, narrator,
                                          context, environment, fun,
                                          fate, worldList, possible,
                                          doors, items, itemsBank,
                                          defeats, blows)
                    elif answer2 == 'run':
                        navigation(limit, name, narrator, context,
                                   environment, fun, fate, worldList,
                                   possible, doors, items, itemsBank,
                                   defeats, blows)
                else:
                    talk("The emptiness of infinite space "
                         "seems somehow darker.")
                    talk("You can feel the deafening void "
                         "within your skull.")
            elif answer2 == 'right':
                talk("You check behind the middle-right "
                     "door.")
                talk("An empty-faced man is directly in "
                     "front of you.")
                talk("This startles you so intensely "
                     "that you blink and fall backwards.")
                talk("There's nothing there when you "
                     "look again. Maybe you're getting "
                     "paranoid.")
            elif answer2 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList, possible,
                           doors, items, itemsBank, defeats, blows)
        elif answer == 'right':
            talk("You turn to the two rightmost doors.")
            talk("You wonder who even made these things.")
            talk("Maybe that's not a question you "
                 "should bother with right now.")
            talk("There are two paths to take. "
                 "LEFT or RIGHT. You can also just RUN.")
            answer3 = ask(('left', 'right', 'run'),
                          "Where will you go?\n")
            if answer3 == 'left':
                talk("You peer behind the first right door.")
                talk("Oh wow! It's a bag of tasty chips!")
                talk("You open them immediately. "
                     "There's only air inside.")
                talk("[The hunger harms you by 1.]")
                blows += 1
            elif answer3 == 'right':
                talk("You sneak behind the second right "
                     "door.")
                talk("You put both hands around the "
                     "frames of the door and try to lift.")
                talk("It doesn't budge. It's sturdier "
                     "than cement. But you feel better "
                     "having tried.")
            elif answer3 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context,
                       environment, fun, fate, worldList,
                       possible, doors, items, itemsBank,
                       defeats, blows)
    talk(f"There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment,
               fun, fate, worldList, possible, doors, items,
               itemsBank, defeats, blows)


def enterKiln(limit, name, narrator, context, environment,
              fun, fate, worldList, possible, doors, items,
              itemsBank, defeats, blows):
    environment = 1
    alive = 1
    quest = 1
    talk("Blistering heat billows from the door as "
         "you open it.")
    while quest == 1:
        talk("Glassy hollows of heat-blasted onyx "
             "surround a massive pit bursting with fire.")
        talk("There are two paths to take. LEFT "
             "and RIGHT. You can also just RUN.")
        answer = ask(('left', 'right', 'run'),
                     "Where will you go?\n")
        if answer == 'left':
            talk("A glowing bud can be seen amid the "
                 "dark, smooth stone.")
            talk("There are two paths to take. "
                 "LEFT or RIGHT, where will you go?\n")
            answer1 = ask(('left', 'right', 'run'),
                          "Where will you go?\n")
            if answer1 == 'left':
                if 'Molten Adamant' in items:
                    talk(f"There's nothing here.")
                else:
                    talk("Wedging the glimmering "
                         "shard free from between the "
                         "sharp crevices, you find the "
                         "Molten Adamant.")
                    items.append('Molten Adamant')
                    talk("\t[The Molten Adamant is now "
                         "in your items!]\n")
            elif answer1 == 'right':
                talk("A single mottlebloom flower "
                     "survives the blistering heat.")
                talk("You are inspired, your wounds "
                     "ache slightly less.")
                talk("\t[You are healed by 1.]\t")
                blows -= 1
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'right':
            talk("Fiberglass wafting from the maw "
                 "of the Kiln's ceaseless discharge "
                 "threatens to make you choke.")
            talk(f"There are two paths to take. LEFT "
                 "and RIGHT. You can also just RUN.")
            answer2 = ask(('left', 'right', 'run'),
                          "Where will you go?\n")
            answer2.lower()
            if answer2 == 'left':
                if alive == 1:
                    talk("Burgeoning flame pours "
                         "from the hollow sockets "
                         "where eyes should be.\n")
                    talk("\tTowering over the melted "
                         "boulders, the Gaulem marches "
                         "towards you.\n")
                    alive = enemyEncounter(environment, fun,
                                           fate, items, itemsBank,
                                           blows)
                    if alive == 0:
                        defeats += 1
                        talk("You have defeated a "
                             "tremendous threat.\n")
                        progressCheck(limit, name, narrator,
                                      context, environment, fun, fate,
                                      worldList, possible, doors,
                                      items, itemsBank, defeats, blows)
                    else:
                        blows += 1
                        if blows < 6:
                            talk("You escape with your "
                                 "life.\n")
                        progressCheck(limit, name, narrator,
                                      context, environment, fun,
                                      fate, worldList, possible,
                                      doors, items, itemsBank,
                                      defeats, blows)
                else:
                    talk("Stone-hewn footsteps are all "
                         "that remain of the pyroclastic Gaulem.")
                    talk(f"No more threat remains here.")
            elif answer2 == 'right':
                talk("Acrid plumes of smoke from the "
                     "roiling magma below stains your "
                     "skin with ash.")
                talk("Better to look elsewhere.")
            elif answer2 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context,
                       environment, fun, fate, worldList, possible,
                       doors, items, itemsBank, defeats, blows)
    talk("There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment,
               fun, fate, worldList, possible, doors, items,
               itemsBank, defeats, blows)


def enterCove(limit, name, narrator, context, environment,
              fun, fate, worldList, possible, doors, items,
              itemsBank, defeats, blows):
    environment = 2
    alive = 1
    quest = 1
    talk("Still though the air is, the humidity"
         " carries a chill that makes your hair stand on end.")
    while quest == 1:
        talk("Dim blue light lapses upward from "
             "hauntingly beautiful pools of water, "
             "illuminating the time-eroded slants of "
             "this cavern.")
        talk("There are two paths to take. "
             "FORWARD and RIGHT. You can also just RUN.")
        answer = ask(('forward', 'right', 'run'),
                     "Where will you go?\n")
        if answer == 'forward':
            talk("You approach the lip of the largest "
                 "reservoir before you.")
            talk("The drop is too steep, and the "
                 "surface too far for you to simply reach in.")
            if 'Coral Wreath' not in items:
                talk("However, something is "
                     "calling to you.")
            talk("This is as far as you can go. "
                 "You can try FORWARD. You can also just RUN.")
            answer1 = ask(('forward', 'run'),
                          "Where will you go?\n")
            if answer1 == 'forward':
                if 'Coral Wreath' in items:
                    talk("There's nothing here.")
                else:
                    talk("You lay flat against the "
                         "cold, damp stone beneath, inching "
                         "forward to hang your arm over the "
                         "cliff.")
                    talk("The sight of the drop below makes "
                         "you hesitate, but your fingers outstretch "
                         "towards this mysterious feeling.")
                    talk("The pool ripples beneath your palm. "
                         "A crown of pale stone rises and grasps "
                         "at your hand with ghostly tendrils of "
                         "water.\n")
                    items.append('Coral Wreath')
                    talk("\t[The Coral Wreath is now in your items!]\n")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context, environment,
                           fun, fate, worldList, possible, doors, items,
                           itemsBank, defeats, blows)
        elif answer == 'right':
            talk("You zig around the first curve between the "
                 "scattered ponds.")
            talk("One of your steps slip against the base of a "
                 "stalagmite, nearly making you lose your footing.")
            talk("Dripping can be heard in every direction from "
                 "here. It bounces contrary to your heartbeat.")
            if (doors < 6) and 'Dirty Ampoule' not in items:
                talk("Something is off. The world feels tilted rightward.")
            talk("There are two paths to take. FORWARD and "
                 "RIGHT. You can also just RUN.")
            answer2 = ask(('forward', 'right', 'run'),
                          "Where will you go?\n")
            if answer2 == 'forward':
                if alive == 1:
                    talk("The path narrows to a crevice. "
                         "You hear your breath eerily close now.")
                    talk("Darkness closes in on you with its "
                         "salt-encrusted teeth.")
                    talk("You can only go FORWARD or RUN.")
                    answer2 = ask(('forward', 'run'),
                                  "Where will you go?\n")
                    if answer2 == 'forward':
                        talk("You turn to your side and "
                             "shimmy as the limestone squeezes "
                             "you like a vice.")
                        talk("There is a pulsing glow at the "
                             "end of the narrow corridor. It feels "
                             "tantalizingly safe.")
                        talk("You stumble and cough as you wrest "
                             "yourself free from the cavernous "
                             "stranglehold.")
                        talk("Your eyes adjust to the only "
                             "source of light.\n")
                        talk("\tTeeth.\n")
                        talk("\tSo very.")
                        talk("\tMany.")
                        talk("\tSpindly.")
                        talk("\tTeeth.\n")
                        talk("\tYou are in the Leviathan's den.\n")
                        alive = alive = enemyEncounter(environment,
                                                       fun, fate, items,
                                                       itemsBank, blows)
                        if alive == 0:
                            defeats += 1
                            talk("You have defeated a "
                                 "tremendous threat.\n")
                            progressCheck(limit, name, narrator,
                                          context, environment, fun,
                                          fate, worldList, possible,
                                          doors, items, itemsBank,
                                          defeats, blows)
                        else:
                            blows += 1
                            if blows < 6:
                                talk("You escape with your life.\n")
                            progressCheck(limit, name, narrator,
                                          context, environment, fun,
                                          fate, worldList, possible,
                                          doors, items, itemsBank,
                                          defeats, blows)
                    elif answer2 == 'run':
                        navigation(limit, name, narrator, context,
                                   environment, fun, fate, worldList,
                                   possible, doors, items, itemsBank,
                                   defeats, blows)
                else:
                    talk("Peering through the passage, the "
                         "Leviathan is little more than a "
                         "rotted pile.")
                    talk("Even the bones have corroded, yet"
                         "somehow only the glow of its lure "
                         "remains.")
            elif answer2 == 'right':
                if 'Dirty Ampoule' not in items:
                    talk("You sense that the universe is smaller "
                         "than it should be.")
                    talk("Scavenging through the dark, you notice "
                         "a glint of swirling, menacing green.\n")
                    items.append('Dirty Ampoule')
                    talk("\t[The Dirty Ampoule is now in your items.]\n")
                else:
                    talk("Stalagtites join the crowd of mineralized "
                         "hazards lining the echoing interior.")
                    talk("You snag against one of their points, "
                         "then trip and slice a nasty gash in your "
                         "leg against another.")
                    talk("\t[You bandage yourself, but not before "
                         "you are harmed by 1.]\n")
                    blows += 1
            elif answer2 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context, environment,
                       fun, fate, worldList, possible, doors, items,
                       itemsBank, defeats, blows)
    talk("There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment, fun, fate,
               worldList, possible, doors, items, itemsBank, defeats, blows)


"""
def enterLab(limit, name, narrator, context, environment, fun, fate,
             worldList, possible, doors, items, itemsBank, defeats, blows):
    environment = 3
    alive = 0
    quest = 0
    while quest == 1:
        talk(f"A comforting nothingness breezes through the "
                       "dark hollow of this vast error.")
        talk(f"The wind makes only noise against the frames "
                       "of the enigmatic doors that stand free of walls.")
        talk(f"There are two paths to take. LEFT and RIGHT, "
                       "where will you go?")
        answer = ask(('left', 'right', 'run'), f"What path "
                                                           "will you take?"
                                                           "\n You can also "
                                                           "just RUN.")
        answer.lower()
        if answer == 'left':
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer1 = ask(('left', 'right', 'run'), f"Where "
                                                                "will you "
                                                                "go?\n")
            answer1.lower()
            if answer1 == 'left':
                talk(f"Vascillating green liquid sloshes "
                               "within a medically sealed syringe.")
                items.append('Dirty Ampoule')
                talk(f"The Dirty Ampoule is now in your items!")
            elif answer1 == 'right':
                talk(f"")
                talk(f"")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'right':
            talk(f"")
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer2 = ask(('left', 'right', 'run'),
                                  f"Where will you go?\n")
            answer2.lower()
            if answer2 == 'left':
                if alive == 1:
                    talk(f"")
                    talk(f"")
                    alive = alive = enemyEncounter(environment, fun,
                                                   fate, items, itemsBank,
                                                   blows)
                    if alive == 0:
                        defeats += 1
                        talk(f"You have defeated a tremendous "
                                       "threat.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                    else:
                        blows += 1
                        if blows < 6:
                            talk(f"You escape with your life.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                else:
                    talk(f"The emptiness of infinite space seems "
                                   "somehow darker.")
                    talk(f"You can feel the deafening void within "
                                   "your skull.")
            elif answer2 == 'right':
                talk(f"")
                talk(f"")
                blows -= 1
            elif answer2 == 'run':
                navigation(limit, name, narrator, context, environment,
                           fun, fate, worldList, possible, doors, items,
                           itemsBank, defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context, environment,
                       fun, fate, worldList, possible, doors, items,
                       itemsBank, defeats, blows)
    talk(f"There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows)


def enterTelos(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows):
    environment = 4
    alive = 0
    quest = 0
    while quest == 1:
        talk(f"A comforting nothingness breezes through the "
                       "dark hollow of this vast error.")
        talk(f"The wind makes only noise against the frames "
                       "of the enigmatic doors that stand free of walls.")
        talk(f"There are two paths to take. LEFT and RIGHT, "
                       "where will you go?")
        answer = ask(('left', 'right', 'run'), f"What path "
                                                           "will you take?\n"
                                                           "You can also just "
                                                           "RUN.")
        answer.lower()
        if answer == 'left':
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer1 = ask(('left', 'right', 'run'), f"Where "
                                                                "will you go?"
                                                                "\n")
            answer1.lower()
            if answer1 == 'left':
                talk(f"A silken scarf floats down upon "
                               "your shoulders, as if destined to.")
                talk(f"Holding it, it wraps around your arm "
                               "as if of its own mind, imbuing you with "
                               "inhuman strength.")
                items.append('Stellated Sash')
                talk(f"The Stellated Sash is now in your items!")
            elif answer1 == 'right':
                talk(f"")
                talk(f"")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'right':
            talk(f"")
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer2 = ask(('left', 'right', 'run'),
                                  f"Where will you go?\n")
            answer2.lower()
            if answer2 == 'left':
                if alive == 1:
                    talk(f"")
                    talk(f"")
                    alive = alive = enemyEncounter(environment, fun,
                                                   fate, items, itemsBank,
                                                   blows)
                    if alive == 0:
                        defeats += 1
                        talk(f"You have defeated a tremendous "
                                       "threat.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                    else:
                        blows += 1
                        if blows < 6:
                            talk(f"You escape with your life.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                else:
                    talk(f"The emptiness of infinite space seems "
                                   "somehow darker.")
                    talk(f"You can feel the deafening void within "
                                   "your skull.")
            elif answer2 == 'right':
                talk(f"")
                talk(f"")
                blows -= 1
            elif answer2 == 'run':
                navigation(limit, name, narrator, context, environment,
                           fun, fate, worldList, possible, doors, items,
                           itemsBank, defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context, environment,
                       fun, fate, worldList, possible, doors, items,
                       itemsBank, defeats, blows)
    talk(f"There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows)


def enterWound(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows):
    environment = 5
    alive = 0
    quest = 0
    while quest == 1:
        talk(f"A comforting nothingness breezes through the "
                       "dark hollow of this vast error.")
        talk(f"The wind makes only noise against the frames "
                       "of the enigmatic doors that stand free of walls.")
        talk(f"There are two paths to take. LEFT and RIGHT, "
                       "where will you go?")
        answer = ask(('left', 'right', 'run'), f"What path "
                                                           "will you take?"
                                                           "\n You can also "
                                                           "just RUN.")
        answer.lower()
        if answer == 'left':
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer1 = ask(('left', 'right', 'run'), f"Where "
                                                                "will you go?"
                                                                "\n")
            answer1.lower()
            if answer1 == 'left':
                talk(f"A swirling cloud of unnerving orange "
                               "dots envelop you.")
                talk(f"You struggle to breathe as you feel "
                               "your body punctured in a thousand places.")
                talk(f"When you open your eyes, the cloud "
                               "has vanished, and you seem unharmed...")
                talk(f"Save for the unsettling flitters "
                               "swimming through your veins.")
                items.append('Cellular Atrophy')
                talk(f"You have Cellular Atrophy. "
                               "Hopefully this journey will not last "
                               "much longer.")
            elif answer1 == 'right':
                talk(f"")
                talk(f"")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList, possible,
                           doors, items, itemsBank, defeats, blows)
            elif answer1 == 'right':
                talk(f"")
                talk(f"")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'right':
            talk(f"")
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer2 = ask(('left', 'right', 'run'),
                                  f"Where will you go?\n")
            answer2.lower()
            if answer2 == 'left':
                if alive == 1:
                    talk(f"")
                    talk(f"")
                    alive = alive = enemyEncounter(environment, fun,
                                                   fate, items, itemsBank,
                                                   blows)
                    if alive == 0:
                        defeats += 1
                        talk(f"You have defeated a tremendous "
                                       "threat.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                    else:
                        blows += 1
                        if blows < 6:
                            talk(f"You escape with your life.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                else:
                    talk(f"The emptiness of infinite space seems "
                                   "somehow darker.")
                    talk(f"You can feel the deafening void within "
                                   "your skull.")
            elif answer2 == 'right':
                talk(f"")
                talk(f"")
                blows -= 1
            elif answer2 == 'run':
                navigation(limit, name, narrator, context, environment,
                           fun, fate, worldList, possible, doors, items,
                           itemsBank, defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context, environment,
                       fun, fate, worldList, possible, doors, items,
                       itemsBank, defeats, blows)
    talk(f"There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows)


def enterSeam(limit, name, narrator, context, environment, fun,
              fate, worldList, possible, doors, items, itemsBank,
              defeats, blows):
    environment = 6
    alive = 0
    quest = 0
    while quest == 1:
        talk(f"A comforting nothingness breezes through the "
                       "dark hollow of this vast error.")
        talk(f"The wind makes only noise against the frames "
                       "of the enigmatic doors that stand free of walls.")
        talk(f"There are two paths to take. LEFT and RIGHT, "
                       "where will you go?")
        answer = ask(('left', 'right', 'run'), f"What path "
                                                           "will you take?"
                                                           "\n You can also "
                                                           "just RUN.")
        answer.lower()
        if answer == 'left':
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer1 = ask(('left', 'right', 'run'), f"Where "
                                                                "will you go?"
                                                                "\n")
            answer1.lower()
            if answer1 == 'left':
                talk(f"Something stirs in your pocket that "
                               "wasn't there before.")
                talk(f"Grasping it, the warmth in your palm "
                               "twitches erratically.")
                talk(f"It stares at you, twice, with only "
                               "one gaze.")
                items.append('Bifurcated Eye')
                talk(f"The Bifurcated Eye is now in your "
                               "inventory.")
            elif answer1 == 'right':
                talk(f"")
                talk(f"")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
            elif answer1 == 'right':
                talk(f"")
                talk(f"")
            elif answer1 == 'run':
                navigation(limit, name, narrator, context,
                           environment, fun, fate, worldList,
                           possible, doors, items, itemsBank,
                           defeats, blows)
        elif answer == 'right':
            talk(f"")
            talk(f"")
            talk(f"There are two paths to take. LEFT and RIGHT. "
                           "You can also just RUN.")
            answer2 = ask(('left', 'right', 'run'),
                                  f"Where will you go?\n")
            answer2.lower()
            if answer2 == 'left':
                if alive == 1:
                    talk(f"")
                    talk(f"")
                    alive = alive = enemyEncounter(environment, fun,
                                                   fate, items, itemsBank,
                                                   blows)
                    if alive == 0:
                        defeats += 1
                        talk(f"You have defeated a tremendous "
                                       "threat.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                    else:
                        blows += 1
                        if blows < 6:
                            talk(f"You escape with your life.")
                        progressCheck(limit, name, narrator, context,
                                      environment, fun, fate, worldList,
                                      possible, doors, items, itemsBank,
                                      defeats, blows)
                else:
                    talk(f"The emptiness of infinite space seems "
                                   "somehow darker.")
                    talk(f"You can feel the deafening void within "
                                   "your skull.")
            elif answer2 == 'right':
                talk(f"")
                talk(f"")
                blows -= 1
            elif answer2 == 'run':
                navigation(limit, name, narrator, context, environment,
                           fun, fate, worldList, possible, doors, items,
                           itemsBank, defeats, blows)
        elif answer == 'run':
            navigation(limit, name, narrator, context, environment,
                       fun, fate, worldList, possible, doors, items,
                       itemsBank, defeats, blows)
    talk(f"There is nothing else to do here.")
    navigation(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows)
"""


# This section has various endings and checks to reach them.
def victoriousEnd(name, narrator, items, defeats, blows):
    talk(f"In spite of all odds, you emerged absolute.")
    talk(f"{name}, your name will be forged in this infinite "
         "abyss as monument. As defiance to fate.")
    talk(f"{narrator} is glad to have served you.\n")
    if len(items) == 1:
        talk(f"And look at that, you did it only with "
             "your Lucky Dice!\n")
        talk(f"\tAll doors have been unlocked.")
        quit()
    else:
        talk(f"\tYour door has been unlocked.")
        quit()


def mortalEnd(name, narrator, defeats, blows):
    talk(f"You burnt your candles at both ends.")
    talk(f"No one will remember your name {name}.")
    talk(f"Except for me, {narrator}.")
    talk(f"I will always care for you.")
    quit()


def anEnd(name, narrator, defeats, blows):
    talk(f"You took {defeats} victories, and leave with "
         f"{blows} scars.")
    talk(f"{narrator} thinks that the greatest victory is survival.")
    talk(f"{name}, you have done well.")
    talk(f"I will always care for you.")
    quit()


def progressCheck(limit, name, narrator, context, environment, fun,
                  fate, worldList, possible, doors, items, itemsBank,
                  defeats, blows):
    if 'SKIPTOEND' in name:
        try:
            defeats = int(name[9])
            blows = int(name[10])
        except ValueError:
            defeats = 0
            blows = 0
    if defeats == 6 or ((doors == 2) and (defeats >= 3)):
        talk(f"{name}, I sense that you're overflowing with "
             "great power.")
        talk(f"You've successfully fulfilled your Gambit. "
             f"{narrator} is proud.")
        talk(f"This was a tremendous task.\nYou must be weary.")
        talk(f"{name}, it is now time for you to retire to the "
             "Veil.\n")
        victoriousEnd(name, narrator, items, defeats, blows)
    elif blows == 6:
        mortalEnd(name, narrator, defeats, blows)
    elif blows == 5:
        talk(f"{name}, please listen to closely.")
        talk(f"{narrator} senses that you are mortally wounded.")
        talk(f"Please ponder this while I say these words.")
        while defeats == 0:
            talk(f"Do not despise me for this. There is no shame "
                 "in abandoning your guilt.")
            talk(f"Preserving your life to fight again another "
                 "day is more important than risking death.")
            state = ask(('yes', 'no'), f"Do you want to "
                        "end your Gambit?")
            if state == 'yes':
                anEnd(name, narrator, defeats, blows)
            elif state == 'no':
                talk(f"Your stubborn will heals you by 2.")
                talk(f"You continue in spite of the humiliation.")
                blows -= 2
                break
            else:
                state = ask(('yes', 'no'), f"I will ask once "
                            "more. Please answer yes or no.")
        while defeats >= 1:
            if defeats == 1:
                talk(f"{name}, you've done well to rid this "
                     "world of a great foe.")
                state = ask(('yes', 'no'), f"Do you want to "
                            "end your Gambit?")
                if state == 'yes':
                    anEnd(name, narrator, defeats, blows)
                elif state == 'no':
                    talk(f"Your stubborn will heals you by 2.")
                    talk(f"You continue in spite of the "
                         "humiliation.")
                    blows -= 2
                    break
                else:
                    state = ask(('yes', 'no'), f"I will ask once more."
                                " Please answer yes or no.")
            elif defeats > 1:
                talk(f"{name}, you've done well to rid this "
                     f"world of {defeats} great foes.")
                state = ask(('yes', 'no'), f"Do you want to end your Gambit?")
                if state == 'yes':
                    anEnd(name, narrator, defeats, blows)
                elif state == 'no':
                    talk(f"Your stubborn will heals you by 2.")
                    talk(f"You continue in spite of the humiliation.")
                    blows -= 2
                    break
                else:
                    state = ask(('yes', 'no'), f"I will ask once more."
                                "Please answer yes or no.")
    elif 'SKIPTOEND' in name:
        talk(f"This is {narrator} checking in.")
        talk(f"{name}, would you like to end your gambit?")
        state = ask(('yes', 'no'), f"Yes or No?")
        if state == 'yes':
            anEnd(name, narrator, defeats, blows)
        elif state == 'no':
            talk(f"{narrator} has changed your name.")
            name = nameGen(fun)
    navigation(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows)


# Transports the player to a new area after a quick check.
# Used directly with the 'navigation' function.
def enterWorld(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows):
    if context == 0:
        enterNexus(limit, name, narrator, context, environment, fun,
                   fate, worldList, possible, doors, items, itemsBank,
                   defeats, blows)
    elif context == 1:
        enterKiln(limit, name, narrator, context, environment, fun,
                  fate, worldList, possible, doors, items, itemsBank,
                  defeats, blows)
    elif context == 2:
        enterCove(limit, name, narrator, context, environment, fun,
                  fate, worldList, possible, doors, items, itemsBank,
                  defeats, blows)
    elif context == 3:
        enterLab(limit, name, narrator, context, environment, fun,
                 fate, worldList, possible, doors, items, itemsBank,
                 defeats, blows)
    elif context == 4:
        enterTelos(limit, name, narrator, context, environment, fun,
                   fate, worldList, possible, doors, items, itemsBank,
                   defeats, blows)
    elif context == 5:
        enterWound(limit, name, narrator, context, environment, fun,
                   fate, worldList, possible, doors, items, itemsBank,
                   defeats, blows)
    elif context == 6:
        enterSeam(limit, name, narrator, context, environment, fun,
                  fate, worldList, possible, doors, items, itemsBank,
                  defeats, blows)
    else:
        talk(f"Are you lost, little one?")


# Prompts the player for going to a new area.
def navigation(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows):
    def blip(doors):
        blipList = []
        blipCount = 0
        while blipCount < doors:
            blipList.append(str(blipCount))
            blipList.append(', ')
            blipCount += 1
        blipList.append('or ')
        blipList.append(str(blipCount))
        blipOutput = "".join(blipList)
        return blipOutput

    blipRead = blip(doors)
    talk(f"You're currently in {worldList[environment]}, "
         f"which means you have {possible} choices.")
    if 'Lucky Dice' not in items:
        talk(f"You notice two shimmering, polygonal stones "
             "on the ground at your feet.\n")
        items.append('Lucky Dice')
        talk(f"\tYou got the Lucky Dice!\n")
        talk(f"Items will be used automatically any time you "
             "have a choice to make.")
        talk(f"Use them to their fullest potential, but "
             "remember that your mind is the most potent item of "
             "all.\n")
        input("\t[PRESS ENTER]\n")
        navigation(limit, name, narrator, context, environment, fun,
                   fate, worldList, possible, doors, items, itemsBank,
                   defeats, blows)
    else:
        talk(f"There's {doors} doors here. Which one will you "
             "go through?")
        talk(f"[This is an alpha! Only doors 0, 1, and 2 "
             "have content in them. Thanks for reading.]")
        context = int(ask(limit, f"Press {blipRead}\n"))
    enterWorld(limit, name, narrator, context, environment, fun,
               fate, worldList, possible, doors, items, itemsBank,
               defeats, blows)


# The opening crawl.
def intro(limit, name, narrator):
    talk(f"Welcome to the Gambit! I'm the voice in "
         f"your head, but you can call me {narrator}!")
    name = ask((''), f"Tell us what you go by, stranger!"
               "\n[Type SkipToEnd + two numbers to debug end.]\n")
    talk(f"Nice to meet'cha {name}.\n")
    return name


# Gets the player started.
def startup(limit, name, narrator, context, environment, fun,
            fate, worldList, possible, doors, items, itemsBank,
            defeats, blows):
    name = intro(limit, name, narrator)
    progressCheck(limit, name, narrator, context, environment, fun,
                  fate, worldList, possible, doors, items, itemsBank,
                  defeats, blows)


# The adventure begins.
def start_the_game():
    fun = magic()
    fate = 0
    name = ''
    narrator = nameGen(fun)
    tS = 20 / 100
    itemsBank = ("Lucky Dice", "Molten Adamant", "Coral Wreath",
                 "Dirty Ampoule", "Stellated Sash", "Cellular Atrophy",
                 "Bifurcated Pupil")
    items = ['']
    state = 0
    context = 0
    worldList = ("The Nexus", "The Kiln", "The Cove", "The Lab", "Telos",
                 "The Wound", "The Seam")
    environment = 0
    possible = 2
    doors = 2
    limit = ('0', '1', '2')
    defeats = 0
    blows = 0
    startup(limit, name, narrator, context, environment, fun,
            fate, worldList, possible, doors, items, itemsBank,
            defeats, blows)
    progressCheck(limit, name, narrator, context, environment,
                  fun, fate, worldList, possible, doors, items, itemsBank,
                  defeats, blows)


if __name__ == '__main__':
    start_the_game()
