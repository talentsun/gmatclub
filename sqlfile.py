import MySQLdb as mdb
import shutil
import os

class SqlFile:
    def __init__(self):
        self.con = mdb.connect('localhost', 'root',
                'nameLR9969', 'gmatclub');
        # con = mdb.connect('localhost', 'root',
        #         '20120811', 'gmatclub');

        cur = self.con.cursor()

        cur.execute("SELECT kaogmat_id,type,kaogamt_set,is_compound,is_sub from RAW_kaoGMAT_Questions where type = 'Integrated Reasoning'")
        data = cur.fetchall()
        for result in data:
            filename = '/home/app_gmatclub/gmatclub/web/eqb/gmatbk/ir/' + result[0] + ".html"
            index_id = self.get_id_count()
            #print filename
            if os.path.exists(filename):
                f = open(filename)
                data = f.read()
                newfile = '/home/app_gmatclub/gmatclub/web/eqb/gmat/ir/' + str(index_id) + ".hmtl"
	        wf = open(newfile,"w")
                wf.write(data)
                f.close()
                wf.close()
                self.insert_into_sql(newfile,result[3],result[4],result[1],result[2])

    def get_id_count(self):
            count = 0
            cur = self.con.cursor()
            result = cur.execute('select @@LAST_INSERT_ID from EQB_Questions')
           # if result[0] == 0:
            #    return count + 1
            #else:
	    print result
            return long(result) + 1

    def insert_into_sql(self,filename,is_compound,is_sub,type,kaogmat_set):
            question_type = 8
            if cmp(type,'Sentence Correction') == 0:
                question_type = 1
            elif cmp(type,'Critical Reasoning') == 0:
                question_type = 2
            elif cmp(type,'Reading Comprehension') == 0:
                question_type = 3
            elif cmp(type,'Data Sufficiency') == 0:
                question_type = 4
            elif cmp(type,'Problem Solving') == 0:
                question_type = 5
            elif cmp(type,'Integrated Reasoning') == 0:
                question_type = 6
            elif cmp(type,'Analytics Writing of Argument') == 0:
                question_type = 7

            question_set = 11
            if cmp(kaogmat_set,'OG10th') == 0:
                question_set = 1
            elif cmp(kaogmat_set,'OG11th') == 0:
                question_set = 2
            elif cmp(kaogmat_set,'OG12th') == 0:
                question_set = 3
            elif cmp(kaogmat_set,'OG13th') == 0:
                question_set = 4
            elif cmp(kaogmat_set,'GWD') == 0:
                question_set = 5
            elif cmp(kaogmat_set,'Knewton') == 0:
                question_set = 6
            elif cmp(kaogmat_set,'Manhattan') == 0:
                question_set = 7
            elif cmp(kaogmat_set,'Princeton') == 0:
                question_set = 8
            elif cmp(kaogmat_set,'Kaplan') == 0:
                question_set = 9
            elif cmp(kaogmat_set,'PREP') == 0:
                question_set = 10
            elif cmp(kaogmat_set,'Other') == 0:
                question_set = 11

            cur = self.con.cursor();
	    sql = "insert into EQB_Questions(is_compound,is_sub,set_id,type_id,content,archive_id) values('" + str(is_compound) + "','" + str(is_sub) + "','" +  str(question_set) + "','" + str(question_type) + "','" + filename +"','" + "0')"
            cur.execute(sql)
            self.con.commit()

