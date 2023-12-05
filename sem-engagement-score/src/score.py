def scorecalc(lec,lab,supp,can):
    lecTotal = 33
    labTotal = 22
    suppTotal = 44
    canTotal = 55
    lecW = 0.3
    labW = 0.4
    suppCanW = 0.15
    score = (lec*lecW/lecTotal+lab*labW/labTotal+supp*suppCanW/suppTotal+can*suppCanW/canTotal) *100
    return round(score)