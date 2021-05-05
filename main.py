import pymongo

client = pymongo.MongoClient("mongodb+srv://maria:adm123@cluster0.qollw.mongodb.net/test?retryWrites=true&w=majority")

db = client.test
col = db.electiondb

def q1(area):
    '''Find the party that received fewest votes in a given constituency.'''
    area = area.lower().strip()
    try:
        pipeline = [
            { '$match': { 'area': area } },
            { '$unwind': '$ukresults' },
            { '$sort': { 'ukresults.ukvotes': 1 }},
            { '$limit': 1 },
            { '$project': {'_id': 0, 'ukresults.party': 1}}
        ]
        result = col.aggregate(pipeline)
        result = list(result)
        return result[0]['ukresults']['party']
    except:
        return 'No records found. Please check if the area was entered correctly.'

def q2():
    '''Find the list of constituencies in which both a Labour candidate (“lab”) and an Ecology candidate (“eco”) 
    stood plus the total number of votes received for the two candidates combined for each such constituency. 
    Return the results in descending order of the combined vote for the two candidates.'''
    pipeline = [
        { '$match': {'$and': [ {'ukresults.party': 'eco'}, {'ukresults.party': 'lab'}]}},
        { '$unwind': '$ukresults' },
        { '$match': {'$or': [ {'ukresults.party': 'eco'}, {'ukresults.party': 'lab'}]}},
        { '$group': {'_id' : '$area', 'lab_eco': {'$sum': '$ukresults.ukvotes'}}},
        { '$project': { '_id': 0, 'area': '$_id', 'total_votes': '$lab_eco' }},
        { '$sort': {'total_votes': -1}},
    ]
    result = col.aggregate(pipeline)
    return result

def q3():
    ''' Find the party that received the highest total number of votes summed across all constituencies.'''
    pipeline = [
        { '$unwind': '$ukresults' },
        { '$group': { '_id' : '$ukresults.party', 'totalvotes': { '$sum' : '$ukresults.ukvotes' }} },
        { '$sort': { 'totalvotes' : -1 } },
        { '$limit': 1},
        { '$project': {'_id': 0, 'party': '$_id'}}
    ]       
    result = col.aggregate(pipeline)
    result = list(result)
    return result[0]['party']

def q4():
    ''' Find the constituencies where the difference in votes for the first and second candidates was less than 1000. 
    Return a list of pairs (c, d) where c is the constituency and d is this difference. 
    Return the results in order of increasing d.'''
    pipeline = [
        { '$unwind': '$ukresults' },
        { '$sort': { 'ukresults.ukvotes': -1 }},
        { '$group': { '_id' : '$area', 'results': {'$push':'$ukresults'} } },
        { '$project': {
            'first': 
                { '$arrayElemAt': [ '$results', 0 ] }, 
            'second': 
                { '$arrayElemAt': [ '$results', 1 ] }}},
        { '$project': {'_id': 0, 'area': '$_id', 'difference': { '$subtract': [ '$first.ukvotes', '$second.ukvotes' ] }}},
        { '$match': {'difference': {'$lt': 1000} }},
        { '$sort': { 'difference': 1 }},
    ]
    result = col.aggregate(pipeline)
    return result 

def q5(party):
    '''Find the list of constituencies where the votes received by a given party was more 
    than 30% of the total number of voters registered for that constituency. 
    Return the results in alphabetical order of constituency names.'''
    party = party.lower().strip()
    try:
        pipeline = [
            { '$unwind': '$ukresults' },
            { '$match': {'ukresults.party': party}}, 
            { '$match': { '$expr': { '$gt': [ "$ukresults.ukvotes" , {'$multiply': [0.3, '$ukelectors']} ] }}},
            { '$project': {'_id': 0, 'area': 1}},
            { '$sort': { 'area': 1 }},
        ]   
        result = col.aggregate(pipeline)
        return result 
    except:
        return 'No records found. Please check if the party was entered correctly.'

def q6():
    '''Find all pairs (c,p) such that party p lost its deposit at constituency c 
    (a party loses its deposit if it wins less than 5% of the votes cast in that constituency).'''
    pipeline = [
        { '$unwind': '$ukresults' },
        { '$group': {
                '_id': '$area', 
                'totalvotes': { '$sum': '$ukresults.ukvotes' }, 
                'ukresults': { '$push': '$ukresults'}   
                } 
        }, 
        { '$unwind': '$ukresults' },
        { '$match': { '$expr': { '$lt': [ '$ukresults.ukvotes', {'$multiply': [0.05, '$totalvotes']} ] }}},
        { '$project': {'_id': 0, 'area': '$_id', 'party': '$ukresults.party'}}
    ]
    result = col.aggregate(pipeline)
    return result

def main():    
    print(f'\nAvailable queries to run:\n'\
        f'1: {q1.__doc__}\n'\
            f'2: {q2.__doc__}\n'\
            f'3: {q3.__doc__}\n'\
            f'4: {q4.__doc__}\n'\
            f'5: {q5.__doc__}\n'\
            f'6: {q6.__doc__}\n')
    while True:
        qnum = input('Enter a query number (see above): ')
        try:
            qnum = int(qnum)
        except:
            print('Not a number')
            continue
        if qnum > 6 or qnum < 1:
            print('Invalid range')
            continue
        break

    # Check if extra arguments needed
    param = ''
    if qnum == 1:
        param = input('This query requires you to enter a constituency area: ')
    if qnum == 5:
        param = input('This query requires you to enter a party: ')

    qnum_function_map = {1: q1(param), 2: q2(), 3: q3(), 4: q4(), 5: q5(param), 6: q6()}

    res = qnum_function_map[qnum]
    if isinstance(res, pymongo.command_cursor.CommandCursor):
        for doc in res:
            print(doc)
    else:
        print(res)

if __name__ == '__main__':
    main()