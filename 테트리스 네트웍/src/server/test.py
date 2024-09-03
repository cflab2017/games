
import datetime as dt
class Test():
    
    # high_score_dict = {
    #     0:{
    #         'name':None,
    #         'score':0,
    #         'date':None},
    #     1:{
    #         'name':None,
    #         'score':0,
    #         'date':None},
    #     2:{
    #         'name':None,
    #         'score':0,
    #         'date':None},
    # }
    high_score_dict = {
        0:{
            'name':None,
            'score':0,
            'date':None},
        1:{
            'name':None,
            'score':0,
            'date':None},
        2:{
            'name':None,
            'score':0,
            'date':None},
    }

    def __init__(self) -> None:
        self.infor = {'최고점수' : self.high_score_dict}
    
    def score_sort(self, name, score):
        print(name)
        
        is_find = 0 
        date = dt.datetime.now()
        for key in self.infor['최고점수']:
            if self.infor['최고점수'][key]['score'] < score:
                is_find = 1
                # break
            if self.infor['최고점수'][key]['name'] == name:
                if self.infor['최고점수'][key]['score'] < score:
                    date_str = f'{date.year}.{date.month}.{date.day}'
                    self.infor['최고점수'][key]['score'] = score
                    self.infor['최고점수'][key]['date'] = date_str
                    is_find = 2
                    break
            
        if is_find:
            score_temp = []
            for key in self.infor['최고점수']:
                score_temp.append(list(self.infor['최고점수'][key].values()))
                
            if is_find == 1:
                date_str = f'{date.year}.{date.month}.{date.day}'
                score_temp.append([name,score,date_str])
                score_temp.sort(key=lambda x:-x[1])
            
            for i,key in enumerate(self.infor['최고점수']):
                self.infor['최고점수'][key]['name'] = score_temp[i][0]
                self.infor['최고점수'][key]['score'] = score_temp[i][1]
                self.infor['최고점수'][key]['date'] = score_temp[i][2]
            print(self.infor)

aa = Test()
aa.sample('aaa',100)
aa.sample('bbb',70)
aa.sample('ccc',90)
aa.sample('eee',200)
aa.sample('aaa',110)
aa.sample('www',110)