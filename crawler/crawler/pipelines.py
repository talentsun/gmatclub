# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from items import Question, CompoundQuestion, Argument

class kaoGMATDBWriterPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CompoundQuestion):
            self.insert_compound_question(item)
        elif isinstance(item, Argument):
            self.insert_argument(item)
        else:
            self.insert_question(item)
        return item
    def insert_question(self, question):
        kaogmat_id = question['id'][0]
        print 'question #%s' % (kaogmat_id)

        type = question['type']
        if type is None:
            type = 'other'
        else:
            type = question['type'][0]

        set = question['set']
        if set is None:
            set = 'other'
        else:
            set = question['set'][0]

        rating = question['rating']
        if rating is None:
            rating = '0.0'
        else:
            rating = question['rating'][0]

        correct_rate = question['correct_rate']
        if correct_rate is None:
            correct_rate = '0.0'
        else:
            correct_rate = question['correct_rate'][0]

        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gmatclub', charset='utf8')
        except Exception, e:
            print e

        try:
            cursor = conn.cursor()
            if not self.exists(kaogmat_id):
                cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, type, `set`, rating, content, answer, explaination, is_compound, is_sub, correct_rate) values(%s, %s, %s, %s, %s, %s, %s, 0, 0, %s)', (kaogmat_id, type, set, rating, question['content'][0], question['answer'][0], question['explaination'][0], correct_rate))
                conn.commit()
            else:
                cursor.execute('update RAW_kaoGMAT_Questions set type=%s, `set`=%s, rating=%s, content=%s, answer=%s, explaination=%s, is_compound=0, is_sub=0, correct_rate=%s where kaogmat_id=%s', (type, set, rating, question['content'][0], question['answer'][0], question['explaination'][0], correct_rate, kaogmat_id))
                conn.commit()
        except Exception,e:
            print e
        cursor.close()
        conn.close()
    def insert_compound_question(self, compound_question):
        kaogmat_id = compound_question['id']
        print 'compound question #%s' % (kaogmat_id)

        type = compound_question['type']
        if type is None:
            type = 'other'

        set = compound_question['set']
        if set is None:
            set = 'other'

        rating = compound_question['rating']
        if rating is None:
            rating = 0.0

        correct_rate = compound_question['correct_rate']
        if correct_rate is None:
            correct_rate = 0.0
        
        compound_question_id = str.join(compound_question['sub_questions'],'-')
        
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gmatclub', charset='utf8')
        except Exception, e:
            print e
            
        try:
            cursor = conn.cursor()
            if not self.exists(compound_question_id):
                cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, type, set, content, is_compound, is_sub) values (%s, %s, %s, %s, 1, 0, %s)', (compound_question_id, type, set, compound_question['article']))
                conn.commit()
            else:
                cursor.execute('update RAW_kaoGMAT_Questions set type=%s, `set`=%s, content=%s, is_compound=1, is_sub=0 where kaogmat_id=%s', (type, set, compound_question['article'], compound_question_id))
                conn.commit()
        except Exception,e:
            print e
        cursor.close()
        
        try:
            cursor = conn.cursor()
            if not self.exists(compound_question['id']):
                cursor.execute('insert into RAW_kaoGMAT_Questions(kaogmat_id, type, set, rating, content, answer, explaination, is_compound, is_sub, correct_rate) values(%s, %s, %s, %s, %s, %s, %s, 0, 1, %s)', (kaogmat_id, type, set, rating, compound_question['content'], compound_question['answer'], compound_question['explaination'], correct_rate))
                conn.commit()
            else:
                cursor.execute('update RAW_kaoGMAT_Questions set type=%s, `set`=%s, rating=%s, content=%s, answer=%s, explaination=%s, is_compound=0, is_sub=1, correct_rate=%s where kaogmat_id=%s', (type, set, rating, compound_question['content'], compound_question['answer'], compound_question['explaination'], correct_rate, compound_question['id']))
                conn.commit()
            insert_or_update_relationship(compound_question_id, compound_question['id'])
        except Exception, e:
            print e
        
        cursor.close()
        conn.close()
    def insert_argument(self,argument):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gmatclub', charset='utf8')
        except Exception,e:
            print e
        
        rating = argument[rating]
        if rating is None:
            rating = 0.0
        
        try:
            cursor = conn.cursor()
            if not self.exists(argument['id']):
                cursor.execute('insert into RAW_kaoGMAT_Questions(kaogamt_id, rating, essay) values(%s, %s, %s)', (argument['id'], rating, argument['essay']))
                conn.commit()
            else:
                cursor.execute('update RAW_kaoGMAT_Questions set rating=%s, essay=%s where kaogmat_id=', (rating, argument['essay'], argument['id']))
                conn.commit()
        except Exception, e:
            print e
        
        cursor.close()
        conn.close()
    def exists(self, question_id):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gmatclub', charset='utf8')
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
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gmatclub', charset='utf8')
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