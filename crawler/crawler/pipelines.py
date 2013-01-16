# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import string
import MySQLdb
from items import Question, CompoundQuestion, Argument

DB_PASSWORD = 'nameLR9969'

class kaoGMATDBWriterPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CompoundQuestion):
            self.insert_compound_question(item)
        elif isinstance(item, Argument):
            self.insert_argument(item)
        else:
            self.insert_question(item)
        return item
    def get_type(self, item):
        type = 'other'
        try:
            type = item['type'][0]
        except Exception,e:
            print e
        return type
    def get_set(self, item):
        set = 'other'
        try:
            set = item['set'][0]
        except Exception,e:
            print e
        return set
    def get_rating(self, item):
        rating = '0.0'
        try:
            rating = item['rating'][0]
        except Exception,e:
            print e
        return rating
    def get_correct_rate(self, item):
        correct_rate = '0.0'
        try:
            correct_rate = item['correct_rate'][0]
        except Exception,e:
            print e
        return correct_rate
    def get_answer(self, item):
        answer = ''
        try:
            answer = item['answer'][0]
        except Exception,e:
            print e
        return answer
    def get_explaination(self, item):
        explaination = ''
        try:
            explaination = item['explaination'][0]
        except Exception,e:
            print e
        return explaination
    def get_id(self, item):
        return item['id'][0]
    def get_content(self, item):
        return item['content'][0]
    def get_article(self, item):
        return item['article'][0]
    def get_essay(self, item):
        return item['essay'][0]
    def insert_question(self, question):
        kaogmat_id = self.get_id(question)
        type = self.get_type(question)
        set = self.get_set(question)
        rating = self.get_rating(question)
        correct_rate = self.get_correct_rate(question)

        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd=DB_PASSWORD, db='gmatclub', charset='utf8')
        except Exception, e:
            print e

        try:
            cursor = conn.cursor()
            if not self.exists(kaogmat_id):
                cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, type, `set`, rating, content, answer, explaination, is_compound, is_sub, correct_rate) values(%s, %s, %s, %s, %s, %s, %s, 0, 0, %s)', (kaogmat_id, type, set, rating, self.get_content(question), self.get_answer(question), self.get_explaination(question), correct_rate))
                conn.commit()
            else:
                cursor.execute('update RAW_kaoGMAT_Questions set type=%s, `set`=%s, rating=%s, content=%s, answer=%s, explaination=%s, is_compound=0, is_sub=0, correct_rate=%s where kaogmat_id=%s', (type, set, rating, self.get_content(question), self.get_answer(question), self.get_explaination(question), correct_rate, kaogmat_id))
                conn.commit()
        except Exception,e:
            print e
        cursor.close()
        conn.close()
    def insert_compound_question(self, compound_question):
        kaogmat_id = self.get_id(compound_question)
        type = self.get_type(compound_question)
        set = self.get_set(compound_question)
        rating = self.get_rating(compound_question)
        correct_rate = self.get_correct_rate(compound_question)
        
        compound_question_id = None
        try:
            compound_question_id = string.join(compound_question['sub_questions'],'-')
        except Exception,e:
            print e
        
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd=DB_PASSWORD, db='gmatclub', charset='utf8')
        except Exception, e:
            print e
         
        if compound_question_id is not None:  
            try:
                cursor = conn.cursor()
                if not self.exists(compound_question_id):
                    cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, type, `set`, content, is_compound, is_sub) values(%s, %s, %s, %s, 1, 0)', (compound_question_id, type, set, self.get_article(compound_question)))
                    conn.commit()
                else:
                    cursor.execute('update RAW_kaoGMAT_Questions set type=%s, `set`=%s, content=%s, is_compound=1, is_sub=0 where kaogmat_id=%s', (type, set, self.get_article(compound_question), compound_question_id))
                    conn.commit()
            except Exception,e:
                print e
        
            try:
                cursor = conn.cursor()
                if not self.exists(kaogmat_id):
                    cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, type, `set`, rating, content, answer, explaination, is_compound, is_sub, correct_rate) values(%s, %s, %s, %s, %s, %s, %s, 0, 1, %s)', (kaogmat_id, type, set, rating, self.get_content(compound_question), self.get_answer(compound_question), self.get_explaination(compound_question), correct_rate))
                    conn.commit()
                else:
                    cursor.execute('update RAW_kaoGMAT_Questions set type=%s, `set`=%s, rating=%s, content=%s, answer=%s, explaination=%s, is_compound=0, is_sub=1, correct_rate=%s where kaogmat_id=%s', (type, set, rating, self.get_content(compound_question), self.get_answer(compound_question), self.get_explaination(compound_question), correct_rate, kaogmat_id))
                    conn.commit()
                self.insert_or_update_relationship(compound_question_id, kaogmat_id)
            except Exception, e:
                print e
        else:
            self.insert_question(compound_question)
        
        cursor.close()
        conn.close()
    def insert_argument(self,argument):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd=DB_PASSWORD, db='gmatclub', charset='utf8')
        except Exception,e:
            print e
        
        kaogmat_id = self.get_id(argument)
        rating = self.get_rating(argument)
        essay = self.get_essay(argument)

        try:
            cursor = conn.cursor()
            if not self.exists(kaogmat_id):
                cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, rating, content, type) values(%s, %s, %s, \'Analytics Writing of Argument\')', (kaogmat_id, rating, essay))
                conn.commit()
            else:
                cursor.execute('update RAW_kaoGMAT_Questions set rating=%s, content=%s, type=%s where kaogmat_id=%s', (rating, essay, 'Analytics Writing of Argument', kaogmat_id))
                conn.commit()
        except Exception, e:
            print e

        cursor.close()
        conn.close()
    def exists(self, question_id):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd=DB_PASSWORD, db='gmatclub', charset='utf8')
        except Exception, e:
            print e
            
        exist = False
        try:
            cursor = conn.cursor()
            count = cursor.execute('select * from RAW_kaoGMAT_Questions where kaogmat_id=%s', (question_id))
            exist = count > 0
        except Exception, e:
            print e
        
        cursor.close()
        conn.close()
        
        return exist
    def insert_or_update_relationship(self, compound_question_id, sub_question_id):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd=DB_PASSWORD, db='gmatclub', charset='utf8')
        except Exception,e:
            print e
        
        try:
            cursor = conn.cursor()
            cursor.execute('delete from RAW_kaoGMAT_Compound_Sub_Questions where sub_question_id=%s', (sub_question_id))
            conn.commit()
            
            cursor.execute('insert into RAW_kaoGMAT_Compound_Sub_Questions(compound_question_id, sub_question_id) values (%s, %s)', (compound_question_id, sub_question_id))
            conn.commit()
        except Exception,e:
            print e
        
        cursor.close()
        conn.close()