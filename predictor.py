import pandas as pd
import joblib

def predictRuns(testInput):
      prediction = 46
      #Reading and Pre-Processing Data
      predictionlst = []
      for j in range(2):
            model_file_path = 'model' + str(j+1) + ".joblib"
            rf = joblib.load(model_file_path)
            
            #Taking Input and Processing Input
            df = pd.read_csv(testInput)
            fileBat =  'batsmen' + str(j+1) + '.csv'
            fileBowl = 'bowler' + str(j+1) + '.csv'
            dfBat = pd.read_csv(fileBat)
            dfBowl = pd.read_csv(fileBowl)
            batsmen = df.iloc[0,4]
            batslst = batsmen.split(",")
            
            avg_bat=0
            for player in batslst:
                player = player[0] + " " +  player.split(" ")[-1][0:]
                if player in dfBat['batsmen'].values:
                    _dfBat = dfBat.loc[dfBat['batsmen']==player]
                    avg_bat += _dfBat.iloc[0]['Rating']
                else:
                    avg_bat += 8.25
            avg_bat = avg_bat/len(batslst)

            wicket = len(batslst)-2      

            bowlers = df.iloc[0,5]
            ballslst = bowlers.split(",")
            avg_bowl = 0
            for player in ballslst:
                player = player[0] + " " +  player.split(" ")[-1][0:]
                if player in dfBowl['bowler'].values:
                    _dfBowl = dfBowl.loc[dfBowl['bowler']==player]
                    avg_bowl += _dfBowl.iloc[0]['Rating']
                else:
                    avg_bowl += 8.25
            avg_bowl = avg_bowl/len(ballslst)

            df = pd.read_csv(testInput)           
            df.replace('MA Chidambaram Stadium, Chepauk','MA Chidambaram Stadium',inplace=True)
            df.replace('MA Chidambaram Stadium, Chepauk, Chennai','MA Chidambaram Stadium',inplace=True)
            df.replace('M.Chinnaswamy Stadium','M Chinnaswamy Stadium',inplace=True)
            df.replace('Feroz Shah Kotla','Arun Jaitley Stadium',inplace=True)
            df.replace('Wankhede Stadium, Mumbai','Wankhede Stadium',inplace=True)
      
            lst = [wicket,avg_bat,avg_bowl,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
            stad=['Arun Jaitley Stadium', 'Eden Gardens', 'M Chinnaswamy Stadium','MA Chidambaram Stadium', 'Wankhede Stadium']
            team =['Chennai Super Kings', 'Delhi Capitals', 'Kolkata Knight Riders', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals','Royal Challengers Bangalore', 'Sunrisers Hyderabad']
            
            for i in range(5):
                if (stad[i]) == df.iloc[0][0]:
                    lst[i+3] = 1.0
            if(1 == df.iloc[0][1]):
                lst[24] = 1.0
            else:
                lst[25] = 1.0
            for i in range(8):
                if (team[i] == df.iloc[0][2]):
                    lst[i+8] = 1.0
            for i in range(8):
                if (team[i] == df.iloc[0][3]):
                    lst[i+16] = 1.0
            inputf = pd.DataFrame([lst])
            y_pred = rf.predict(inputf)
            predictionlst.append(int(y_pred[0]))

      prediction =  (0.6 * predictionlst[0] + 0.4 * predictionlst[1])
      return round(prediction)