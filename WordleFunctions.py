from matplotlib import pyplot
import pandas as pd


def create_set(txt_dir):
    """Takes text file of possible words and returns a set of those words.

    Keyword arguments:
    txt_dir = The directory of the text file
    """
    
    set1 = set(line.strip() for line in open(txt_dir))
    
    new_set = set()
    for i in set1:
        if len(i) == 5:
            new_set.add(i)
    return new_set


def remove_misses(prev_set ,guess = '', result = ''):
    """Takes a set of possible words, a guess, and the result of that guess and returns a set of possible words without any of the blacked out guesses (misses).

    Keyword arguments:
    prev_set = Set of possible words
    guess = Lowercase 5 letter word that is guessed (default = '')
    result = Result of guess in lowercase 5 letter form (b for blacked out tiles, y for yellow tiles, and g for green tiles) (default = '')
    """
    
    possible_set = prev_set
        
    temp_dict = dict()
    possible_set2 = set()       
        
    for n in range(0,5):
        temp_dict[guess[n]] = result[n]
        
    possible_set2 = possible_set.copy()
    for w in possible_set:
        word_check=0
        for l in guess:
            if temp_dict[l]=="b":
                if (l==w[0] or l==w[1] or l==w[2] or l==w[3] or l==w[4]) and word_check==0:
                    possible_set2.remove(w)
                    word_check += 1
        
    return possible_set2


def letter_prop_df(prev_set, infunc = False):
    """Takes a set of possible words and returns pandas DataFrame of every letter and its frequency and proportion in the possible set of words.

    Keyword arguments:
    prev_set = Set of possible words
    infuc = Boolean, returns a dict of the information instead (default = False)
    """
    
    possible_set = prev_set
    
    new_dict = dict()
    for a in 'abcdefghijklmnopqrstuvwxyz':
        tot = 0
        for b in prev_set:
            tot += b.count(a)
        new_dict[a]=tot
    
    newt = 0
    for i in list(new_dict.values()):
        newt += i
    
    new_dict2 = dict()
    for key in new_dict.keys():
            new_dict2[key] = [new_dict[key], new_dict[key]/newt]
            
    letter_df=pd.DataFrame.from_dict(new_dict2, orient='index', columns = ['Frequency', 'Proportion'])
    letter_df.reset_index(inplace=True)
    letter_df = letter_df.rename(columns = {'index':'Letter'})
    
    if infunc == False:
        return letter_df
    if infunc == True:
        return new_dict2
    
def letter_dist_df(prev_set):
    """Takes a set of possible words and returns pandas DataFrame of every letter and its frequency and proportion of that letter, given its position.

    Keyword arguments:
    prev_set = Set of possible words
    """
    
    
    possible_set = prev_set.copy()
    new_dict2 = letter_prop_df(possible_set, infunc = True)
        
    new_dict3 = dict()
    for key in new_dict2.keys():
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
        p5 = 0
        for w in possible_set:
            if key in w:
                if w[0]==key:
                    p1 +=1
                if w[1]==key:
                    p2 +=1
                if w[2]==key:
                    p3 +=1
                if w[3]==key:
                    p4 +=1
                if w[4]==key:
                    p5 +=1
    
        new_dict3[key] = [p1, p1/new_dict2[key][0], p2, p2/new_dict2[key][0], p3, p3/new_dict2[key][0], p4, p4/new_dict2[key][0], p5, p5/new_dict2[key][0]]
        
    letter_dist_df=pd.DataFrame.from_dict(new_dict3, orient='index', columns = ['p1 Frequency', 'p1 Proportion', 'p2 Frequency', 'p2 Proportion', 'p3 Frequency', 'p3 Proportion', 'p4 Frequency', 'p4 Proportion', 'p5 Frequency', 'p5 Proportion'])
    letter_dist_df.reset_index(inplace=True)
    letter_dist_df = letter_dist_df.rename(columns = {'index':'Letter'})
    
    return letter_dist_df


def single_let_dist_viz(prev_set):
    """Takes a set of possible words then asks for an input, and returns a graph of the input letter's position.

    Keyword arguments:
    prev_set = Set of possible words
    """
    
    a = input("Enter a lowercase letter:")
    letter1_dist_df = letter_dist_df(prev_set)
    temp_df = letter1_dist_df[letter1_dist_df.Letter == a]
    temp_df = temp_df.select_dtypes(exclude="int64")
    data = list(temp_df.iloc[0,1:6])
    names = ['Letter 1', 'Letter 2', 'Letter 3', 'Letter 4', 'Letter 5']
    temp_df = pd.DataFrame(data=data,index=names)
    
    pyplot.bar(x = temp_df.index, height = temp_df[0])
    pyplot.ylabel("Proportion of Letter Positions")
    pyplot.title("{}'s Position by Proportion".format(a))

    pyplot.show()
    
    
def get_greens(prev_set,guess = '', result = ''):
    """Takes a set of possible words, a guess, and the result of that guess and returns a set of possible words with words that have the green letters in the same position as the guess.

    Keyword arguments:
    prev_set = Set of possible words
    guess = Lowercase 5 letter word that is guessed (default = '')
    result = Result of guess in lowercase 5 letter form (b for blacked out tiles, y for yellow tiles, and g for green tiles) (default = '')
    """
    
    possible_set = prev_set
    
    temp_dict = dict()
    possible_set2 = set()
    g_letters = result.count('g')
    
    for n in range(0,5):
        temp_dict[guess[n]] = result[n]
        
    g_letloc_list = list()
    for n in range(0,5):
        if result[n]=='g':
            g_letloc_list.append([guess[n],n])
    
    for w in possible_set:
        if g_letters == 0:
            possible_set2.add(w)
            
        elif g_letters > 0:
            if g_letters ==1:
                if g_letloc_list[0][0] == w[g_letloc_list[0][1]]:
                    possible_set2.add(w)
            if g_letters ==2:
                if g_letloc_list[0][0] == w[g_letloc_list[0][1]] and g_letloc_list[1][0] == w[g_letloc_list[1][1]]:
                    possible_set2.add(w)
            if g_letters ==3:
                if g_letloc_list[0][0] == w[g_letloc_list[0][1]] and g_letloc_list[1][0] == w[g_letloc_list[1][1]] and g_letloc_list[2][0] == w[g_letloc_list[2][1]]:
                    possible_set2.add(w)
            if g_letters ==4:
                if g_letloc_list[0][0] == w[g_letloc_list[0][1]] and g_letloc_list[1][0] == w[g_letloc_list[1][1]] and g_letloc_list[2][0] == w[g_letloc_list[2][1]] and g_letloc_list[3][0] == w[g_letloc_list[3][1]]:
                    possible_set2.add(w)
            if g_letters ==5:
                if g_letloc_list[0][0] == w[g_letloc_list[0][1]] and g_letloc_list[1][0] == w[g_letloc_list[1][1]] and g_letloc_list[2][0] == w[g_letloc_list[2][1]] and g_letloc_list[3][0] == w[g_letloc_list[3][1]] and g_letloc_list[4][0] == w[g_letloc_list[4][1]]:
                    possible_set2.add(w)
                    
    return possible_set2


def get_yellows(prev_set, guess = '', result = ''):
    """Takes a set of possible words, a guess, and the result of that guess and returns a set of possible words with words that have the yellow letters in the word, but not in the same position as the guess.

    Keyword arguments:
    prev_set = Set of possible words
    guess = Lowercase 5 letter word that is guessed (default = '')
    result = Result of guess in lowercase 5 letter form (b for blacked out tiles, y for yellow tiles, and g for green tiles) (default = '')
    """
    
    possible_set = prev_set
        
    temp_dict = dict()
    possible_set2 = set()
    y_letters = result.count('y')        
    
    for n in range(0,5):
        temp_dict[guess[n]] = result[n]
        
    y_letloc_list = list()
    for n in range(0,5):
        if result[n]=='y':
            y_letloc_list.append([guess[n],n])
            
    for w in possible_set:
        if y_letters == 0:
            possible_set2.add(w)
            
        elif y_letters > 0:
            if y_letters ==1:
                if y_letloc_list[0][0] != w[y_letloc_list[0][1]] and y_letloc_list[0][0] in w:
                    possible_set2.add(w)
            if y_letters ==2:
                if y_letloc_list[0][0] != w[y_letloc_list[0][1]] and y_letloc_list[1][0] != w[y_letloc_list[1][1]] and y_letloc_list[0][0] in w and y_letloc_list[1][0] in w:
                    possible_set2.add(w)
            if y_letters ==3:
                if y_letloc_list[0][0] != w[y_letloc_list[0][1]] and y_letloc_list[1][0] != w[y_letloc_list[1][1]] and y_letloc_list[2][0] != w[y_letloc_list[2][1]] and y_letloc_list[0][0] in w and y_letloc_list[1][0] in w and y_letloc_list[2][0] in w:
                    possible_set2.add(w)
            if y_letters ==4:
                if y_letloc_list[0][0] != w[y_letloc_list[0][1]] and y_letloc_list[1][0] != w[y_letloc_list[1][1]] and y_letloc_list[2][0] != w[y_letloc_list[2][1]] and y_letloc_list[3][0] != w[y_letloc_list[3][1]] and y_letloc_list[0][0] in w and y_letloc_list[1][0] in w and y_letloc_list[2][0] in w and y_letloc_list[3][0]:
                    possible_set2.add(w)
            if y_letters ==5:
                if y_letloc_list[0][0] != w[y_letloc_list[0][1]] and y_letloc_list[1][0] != w[y_letloc_list[1][1]] and y_letloc_list[2][0] != w[y_letloc_list[2][1]] and y_letloc_list[3][0] != w[y_letloc_list[3][1]] and y_letloc_list[4][0] != w[y_letloc_list[4][1]] and y_letloc_list[0][0] in w and y_letloc_list[1][0] in w and y_letloc_list[2][0] in w and y_letloc_list[3][0] in w and y_letloc_list[4][0] in w:
                    possible_set2.add(w)
                    
    return possible_set2


def full_guess_set(prev_set, guess = '', result = ''):
    """Takes a set of possible words, a guess, and the result of that guess and returns all possible guesses after removing misses and accounting for green and yellow letters.

    Keyword arguments:
    prev_set = Set of possible words
    guess = Lowercase 5 letter word that is guessed (default = '')
    result = Result of guess in lowercase 5 letter form (b for blacked out tiles, y for yellow tiles, and g for green tiles) (default = '')
    """
    
    guess = str(guess)
    result = str(result)
    fullset = get_yellows(get_greens(remove_misses(prev_set=prev_set, guess=guess, result=result), guess=guess, result=result), guess=guess, result=result)
    return fullset


def get_word_scores(prev_set):
    """Takes a set of possible words and returns a pandas DataFrame with "scores" for each word. Green letters is the expected number of green letters for each word and the adjusted score penalizes words that have repeat letters so words that narrow down possible words are higher in the rankings.

    Keyword arguments:
    prev_set = Set of possible words
    """
    
    new_dict = dict()
    for a in 'abcdefghijklmnopqrstuvwxyz':
        tot = 0
        for b in prev_set:
            if a in b:
                tot += 1
        new_dict[a]=tot
        
    newt = 0
    for i in list(new_dict.values()):
        newt += i
    
    new_dict2 = dict()
    for key in new_dict.keys():
            new_dict2[key] = [new_dict[key], new_dict[key]/newt]

    new_dict3 = dict()
    for key in new_dict2.keys():
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
        p5 = 0
        for w in prev_set:
            if key in w:
                if w[0]==key:
                    p1 +=1
                if w[1]==key:
                    p2 +=1
                if w[2]==key:
                    p3 +=1
                if w[3]==key:
                    p4 +=1
                if w[4]==key:
                    p5 +=1
    
        new_dict3[key] = [new_dict2[key][1], p1/len(prev_set), p2/len(prev_set), p3/len(prev_set), p4/len(prev_set), p5/len(prev_set)]
    
    score_dict = dict()
    for w in prev_set:
        green_score = 0
        for n in range(0,5):
            green_score = green_score + new_dict3[w[n]][n+1] # non conditional probability that any of the letters in the word will be green
                    
        if len(w) != len(''.join(set(w))):
            double_let = True
        else:
            double_let = False        
        
        score_dict[w] = [green_score, double_let, green_score-(double_let/2)]
    
    best_guess_df=pd.DataFrame.from_dict(score_dict, orient='index', columns = ['Green Letters', 'Repeat Letters', 'Adj. Green Score'])
    best_guess_df.reset_index(inplace=True)
    best_guess_df = best_guess_df.rename(columns = {'index':'Possible Words'})
    best_guess_df = best_guess_df.sort_values('Adj. Green Score', ascending = False, ignore_index=True)
    
    return best_guess_df


def manual_robo_guesser(prev_set):
    """Takes a set of possible words and prints the optimal guess. Then it asks for the results of each guess until the puzzle is solved or can't be completed in 6 guesses. Useful for playing without knowing the answer.

    Keyword arguments:
    prev_set = Set of possible words
    """
    
    ps = prev_set
    ng = 1
    result = ''
    while result != 'ggggg' and ng <= 6 :
        tdf = get_word_scores(ps)
        guess = str(tdf.iloc[0,0])
        print("My guess ({}/6) is: {}".format(ng,guess))
        result=str(input("Result:"))
        ps = full_guess_set(prev_set=ps, guess=guess,result=result)
        ng+=1
    if result == 'ggggg' and ng <=7:
        print("SOLVED! The computer completed today's Wordle in {} guesses. The correct answer was '{}'.".format(ng-1, guess))
    else:
        print("UH OH! The computer couldn't solve today's Wordle within 6 guesses. It's last guess was '{}' with the result of {}".format(guess, result))
        

def get_result(guess, answer):
    """Takes a guess and the answer and returns the results in lowercase 5 letter form (b for blacked out tiles, y for yellow tiles, and g for green tiles).

    Keyword arguments:
    guess = Lowercase 5 letter word that is guessed
    answer = Lowercase 5 letter word that is the answer to the puzzle
    """
    result_list = ['b', 'b', 'b', 'b', 'b']
    for n in range(0,5):
        if guess[n] not in answer:
            continue
        elif guess[n] == answer[n]:
            result_list[n] = 'g'
        elif guess[n] in answer:
            result_list[n] = 'y'
            
            # this is the simple definition of y that works in my robosolver
            
    result = ''.join(result_list)
    return result


def auto_robo_guesser(prev_set, answer, inloop = False):
    """Takes a set of possible words and the answer to the puzzle and plays through it using optimal guesses. Useful for seeing the optimal guesses when you already know the answer or for testing how quickly and accurates the algorithm get the correct answers (see inloop Keyword).

    Keyword arguments:
    prev_set = Set of possible words
    inloop = Boolean, returns how many guesses it took using optimal guesses (or 7 if wrong). Can be use to determine accuracy and average number of guesses (default = False)
    """
    
    answer = str(answer)
    ps = prev_set
    ng = 1
    result = ''
    while result != 'ggggg' and ng <= 6 :
        tdf = get_word_scores(ps)
        guess = str(tdf.iloc[0,0])
        if inloop == False:
            print("My guess ({}/6) is: {}".format(ng,guess))
        result= get_result(guess, answer)
        if inloop == False:
            print("Result of guess {} is: {}".format(ng, result))
        ps = full_guess_set(prev_set=ps, guess=guess,result=result)
        ng+=1
        
    if inloop == False:
        if result == 'ggggg' and ng <=7:
            print("SOLVED! The computer completed today's Wordle in {} guesses. The correct answer was '{}'.".format(ng-1, guess))
        else:
            print("UH OH! The computer couldn't solve today's Wordle within 6 guesses. It's last guess was '{}' with the result of {}".format(guess, result))
    else:
        return ng-1