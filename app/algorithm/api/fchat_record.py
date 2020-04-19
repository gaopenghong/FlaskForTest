from app.algorithm.api.fchat_static import *
#from app.algorithm.models.fchat_model import *
from app.algorithm.models.config_model import *
import time

class Records(Forchat):
    @staticmethod
    def fchat_record():

        Forchat.match_all()
        rate = Forchat.static()
        rate1 = rate[0]
        rate2 = rate[1]
        rate3 = rate[2]
        rate4 = rate[3]
        rate5 = rate[4]

        key_value = db.session.query(Indexconf.key,Indexconf.value).filter_by(type=1).all()
        for i in range(len(key_value)):
            s = (key_value[i])
            index = int(s[0])
            index_value = float(s[1])
            if index == 1:
                if rate1 >= index_value:
                    run_result1 = 'true'
                else:
                    run_result1 = 'false'

            elif index == 2:
                if rate2 >= index_value:
                    run_result2 = 'true'
                else:
                    run_result2 = 'false'

            elif index == 3:
                if rate3 >= index_value:
                    run_result3 = 'true'
                else:
                    run_result3 = 'false'

            elif index == 4:
                if rate4 >= index_value:
                    run_result4 = 'true'
                else:
                    run_result4 = 'false'

            elif index == 5:
                if rate5 >= index_value:
                    run_result5 = 'true'
                else:
                    run_result5 = 'false'

        if run_result1 == 'true' and run_result2 == 'true' and run_result3 == 'true' and run_result4 == 'true' and run_result5 == 'true':
            run_result = 'true'
        else:
            run_result = 'false'

        return run_result, rate


if __name__=='__main__':
    Records.fchat_record()