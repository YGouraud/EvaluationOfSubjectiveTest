# Generated with SMOP  0.41
from libsmop import *
# classify_lab_to_lab.m

    
@function
def classify_lab_to_lab(testname=None,labA=None,labB=None,*args,**kwargs):
    varargin = classify_lab_to_lab.varargin
    nargin = classify_lab_to_lab.nargin

    # labA and labB list the ratings for each lab on the identical sequences,
# rated by different subjects. 
# calculate the differnt results of conclusions by the two labs for all
# pairs of sequences.
    
    num_pvs=size(labA,1)
# classify_lab_to_lab.m:7
    conclude[1]=0
# classify_lab_to_lab.m:9
    
    conclude[2]=0
# classify_lab_to_lab.m:10
    
    conclude[3]=0
# classify_lab_to_lab.m:11
    
    conclude[4]=0
# classify_lab_to_lab.m:12
    
    conclude[5]=0
# classify_lab_to_lab.m:13
    
    for cnt1 in arange(1,num_pvs).reshape(-1):
        for cnt2 in arange(cnt1 + 1,num_pvs).reshape(-1):
            ans1=ttest(labA(cnt1,arange()),labA(cnt2,arange()))
# classify_lab_to_lab.m:17
            ans2=ttest(labB(cnt1,arange()),labB(cnt2,arange()))
# classify_lab_to_lab.m:18
            mosA1=nanmean(labA(cnt1,arange()))
# classify_lab_to_lab.m:19
            mosA2=nanmean(labA(cnt2,arange()))
# classify_lab_to_lab.m:20
            mosB1=nanmean(labB(cnt1,arange()))
# classify_lab_to_lab.m:21
            mosB2=nanmean(labB(cnt2,arange()))
# classify_lab_to_lab.m:22
            if ans1 == 1 and ans2 == 1 and mosA1 > mosA2 and mosB1 > mosB2:
                conclude[1]=conclude(1) + 1
# classify_lab_to_lab.m:24
            else:
                if ans1 == 1 and ans2 == 1 and mosA1 < mosA2 and mosB1 < mosB2:
                    conclude[1]=conclude(1) + 1
# classify_lab_to_lab.m:26
                else:
                    if ans1 == 0 and ans2 == 0:
                        conclude[2]=conclude(2) + 1
# classify_lab_to_lab.m:28
                    else:
                        if ans1 == 1 and ans2 == 0:
                            conclude[3]=conclude(3) + 1
# classify_lab_to_lab.m:30
                        else:
                            if ans1 == 0 and ans2 == 1:
                                conclude[4]=conclude(4) + 1
# classify_lab_to_lab.m:32
                            else:
                                conclude[5]=conclude(5) + 1
# classify_lab_to_lab.m:33
    
    fprintf('\n\n%s, ',testname)
    fprintf('%d PVSs, ',size(labA,1))
    fprintf('Subjects: %d vs %d\n',size(labA,2),size(labB,2))
    fprintf('%4.0f%% Agree Rank, ',round(dot(100,conclude(1)) / sum(conclude)))
    fprintf('%4.0f%% Agree Tie, ',round(dot(100,conclude(2)) / sum(conclude)))
    fprintf('%4.0f%% Unconfirmed (labA), ',round(dot(100,conclude(3)) / sum(conclude)))
    fprintf('%4.0f%% Unconfirmed (labB), ',round(dot(100,conclude(4)) / sum(conclude)))
    fprintf('%4.2f%% Disagree\n',dot(100,conclude(5)) / sum(conclude))
    return conclude
    
if __name__ == '__main__':
    pass
    