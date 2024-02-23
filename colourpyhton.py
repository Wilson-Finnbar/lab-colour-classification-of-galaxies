#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
plt.rcParams.update({'font.size': 10})

# %%
#Part A galaxy types and colours

pA = pd.read_csv('Data/PartA.csv')

a_ug = pA['u'] - pA['g']
a_gr = pA['g'] - pA['r']

bcx = a_ug[a_ug>1.6]
bcy = a_gr[a_ug>1.6]

rcx = a_ug[a_ug<1.6]
rcy = a_gr[a_ug<1.6]

x =  np.arange(1,2.2,0.1)
y = 2.2-x

fig1 = plt.figure(figsize=(5,3.3))
ax1 = fig1.add_subplot(111)

for i in range(len(a_gr)):
    a = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)']
    if a[i] == '(a)':
        ax1.annotate(f"{a[i]}",(a_ug[i]-0.023,a_gr[i]+0.04))
    elif a[i] == '(i)':
        ax1.annotate(f"{a[i]}",(a_ug[i]-0.02,a_gr[i]-0.07))
    elif a[i] == '(g)':
        ax1.annotate(f"{a[i]}",(a_ug[i]-0.02,a_gr[i]-0.07))
    else:
        ax1.annotate(f"{a[i]}",(a_ug[i]-0.023,a_gr[i]+0.04))


ax1.plot(rcx,rcy,'ro',alpha=0.4)
ax1.plot(bcx,bcy,'bo',alpha=0.4)
ax1.plot(x,y,'k--',alpha=0.3)
ax1.set_xlim(1,2.2)
ax1.set_ylim(0,1.2)
ax1.set_xlabel('(u-g)')
ax1.set_ylabel('(g-r)')
plt.tight_layout()
plt.savefig('Data/parta.pdf')

df1 = pA[['u','g','r']]
df1.insert(loc=0, column='Galaxy', value=a)
df1.reset_index(drop=True, inplace=True)
df1 = df1.transpose()

print(list(range(1,21)))
# %%
# Part B Clusters of Galaxies
b = pd.read_csv("Data/PartB.csv")
b2 = pd.read_csv('Data/PartB2.csv')
b2 = b2[b2['type'] == 3]

df2 = b[['ra','dec','u','g','r']]
df2.insert(loc=0, column='Galaxy', value=list(range(1,22)))
df2.set_index('Galaxy', inplace=True)
print(df2.to_latex(float_format="%.3f"))

x =  np.arange(-6,8,0.1)
y = 2.2-x

fig2 = plt.figure(figsize=(5,3.3))
ax2 = fig2.add_subplot(111)

ax2.plot(b['u']-b['g'],b['g']-b['r'],'go',alpha=0.3, label='self select')
ax2.plot(b2['u']-b2['g'],b2['g']-b2['r'],'bo',alpha=0.1,label='radial search')
ax2.plot(x,y,'k--',alpha=0.3)
ax2.add_patch(Rectangle((1,0.6),1.6,0.6, fc='none',ec='r',lw=1,label='zoomed plot',zorder=3))
ax2.set_xlim(-6,8)
ax2.set_ylim(-6,10)
ax2.set_xlabel('(u-g)')
ax2.set_ylabel('(g-r)')
ax2.legend()
plt.tight_layout()
plt.savefig('Data/partb1.pdf')

fig3 = plt.figure(figsize=(5,3.3))
ax3 = fig3.add_subplot(111)

ax3.plot(b['u']-b['g'],b['g']-b['r'],'go',alpha=0.3, label='self select')
ax3.plot(b2['u']-b2['g'],b2['g']-b2['r'],'bo',alpha=0.1,label='radial search')
ax3.plot(x,y,'k--',alpha=0.3)
ax3.set_xlim(1,2.6)
ax3.set_ylim(0.6,1.2)
ax3.set_xlabel('(u-g)')
ax3.set_ylabel('(g-r)')
ax3.legend()
plt.tight_layout()
plt.savefig('Data/partb1zoom.pdf')

b2['u-g'] = (b2['u']-b2['g'])
b2['g-r'] = (b2['g']-b2['r'])
pos = b2[['u-g','g-r']].to_numpy()

above = 0
a = np.array([-7,9.2])
b = np.array([9,-6.8])

for i in range(len(b2.axes[0])):
    if np.cross(pos[i]-a,b-a) < 0:
        above += 1

print(f"above: {above}\nbellow: {len(b2.axes[0])-above}")
# %%
#Part B 2 u-r properties

g1519 = b2[b2['g'].between(15,19)]
g1923 = b2[b2['g'].between(19,23)]
print(f"15<g<19: {len(g1519.axes[0])}\n19<g<23: {len(g1923.axes[0])}\n")

g1519['u-r'] = (g1519['u']-g1519['r'])
g1923['u-r'] = (g1923['u']-g1923['r'])
print(f"15<g<19 mean u-r: {g1519['u-r'].mean() :.3f} \n19<g<23 mean u-r: {g1923['u-r'].mean() :.3f}\n")

fig4 = plt.figure(figsize=(5,3.3))
ax4 = fig4.add_subplot(111)

ax4.plot(g1519['u-r'],g1519['g'],c='cornflowerblue',marker='o',lw=0,alpha=0.3,label='15<g<19')
ax4.axvline(x=g1519['u-r'].mean(),c='cornflowerblue',ls='--')
ax4.plot(g1923['u-r'],g1923['g'],c='tab:pink',marker='o',lw=0,alpha=0.3,label='19<g<23')
ax4.axvline(x=g1923['u-r'].mean(),c='tab:pink',ls='--')
ax4.set_xlim(-4,8)
ax4.set_ylim(15,24)
ax4.set_xlabel('u-r')
ax4.set_ylabel('g')
ax4.legend(loc='best')
plt.tight_layout()
plt.savefig("Data/urproperties.pdf")
# %%
#Part C: Tracking galaxy colours as a function of redshift
A2255 = pd.read_csv('Data/PartB2.csv')
A2255 = A2255[A2255['type'] == 3]

A0023 = pd.read_csv('Data/Abell0023.csv')
A0023 = A0023[A0023['type'] == 3]

A0267 = pd.read_csv('Data/Abell0267.csv')
A0267 = A0267[A0267['type'] == 3]

A2255['u-g'] = (A2255['u']-A2255['g'])
A2255['g-r'] = (A2255['g']-A2255['r'])

A0023['u-g'] = (A0023['u']-A0023['g'])
A0023['g-r'] = (A0023['g']-A0023['r'])

A0267['u-g'] = (A0267['u']-A0267['g'])
A0267['g-r'] = (A0267['g']-A0267['r'])

fig5 = plt.figure(figsize=(5,3.3))
ax5 = fig5.add_subplot(111)

ax5.plot(A2255['u-g'],A2255['g-r'],c='mediumpurple',marker='.',lw=0,alpha=0.3,label='Abell 2255')
ax5.plot(A0023['u-g'],A0023['g-r'],c='palegreen',marker='.',lw=0,alpha=0.3,label='Abell 0023')
ax5.plot(A0267['u-g'],A0267['g-r'],c='crimson',marker='.',lw=0,alpha=0.3,label='Abell 0267')
ax5.plot(x,y,'k--',alpha=0.3)
ax5.set_xlim(-6,8)
ax5.set_ylim(-8,10)
ax5.set_xlabel('u-g')
ax5.set_ylabel('g-r')
ax5.legend(loc='best')
plt.tight_layout()
plt.savefig("Data/partcallgalaxy.pdf")
# %%
#Part C: histograms 
A2255['u-r'] = (A2255['u']-A2255['r'])
A0023['u-r'] = (A0023['u']-A0023['r'])
A0267['u-r'] = (A0267['u']-A0267['r'])

hisbins = np.linspace(-5,15,num=50)

plt.figure(figsize=(3.5,2.5))
plt.hist(A2255['u-r'],bins=hisbins,color='mediumpurple',alpha=0.5)
plt.axvline(x=A2255['u-r'].mean(),c='mediumpurple',ls='--')
plt.xlabel('u-r')
plt.ylabel('Frequency')
plt.xlim(-5,15)
plt.ylim(0,100)
plt.tight_layout()
plt.savefig("Data/A2255hist.pdf")

plt.figure(figsize=(3.5,2.5))
plt.hist(A0023['u-r'],bins=hisbins,color='palegreen',alpha=0.5)
plt.axvline(x=A0023['u-r'].mean(),c='palegreen',ls='--')
plt.xlabel('u-r')
#plt.ylabel('Frequency')
plt.xlim(-5,15)
plt.ylim(0,100)
plt.tight_layout()
plt.savefig("Data/A0023hist.pdf")

plt.figure(figsize=(3.5,2.5))
plt.hist(A0267['u-r'],bins=hisbins,color='crimson',alpha=0.5)
plt.axvline(x=A0267['u-r'].mean(),c='crimson',ls='--')
plt.xlabel('u-r')
#plt.ylabel('Frequency')
plt.xlim(-5,15)
plt.ylim(0,100)
plt.tight_layout()
plt.savefig("Data/A0267hist.pdf")

# %%
#Part C: values

pA2255 = A2255[['u-g','g-r']].to_numpy()
pA0023 = A0023[['u-g','g-r']].to_numpy()
pA0267 = A0267[['u-g','g-r']].to_numpy()

a = np.array([-7,9.2])
b = np.array([9,-6.8])

a2255 = 0
a0023 = 0
a0267 = 0

for i in range(len(A2255.axes[0])):
    if np.cross(pA2255[i]-a,b-a) < 0:
        a2255 += 1

for i in range(len(A0023.axes[0])):
    if np.cross(pA0023[i]-a,b-a) < 0:
        a0023 += 1

for i in range(len(A0267.axes[0])):
    if np.cross(pA0267[i]-a,b-a) < 0:
        a0267 += 1

print(a2255,a0023,a0267)

fig6 = plt.figure(figsize=(5,3.3))
ax6 = fig6.add_subplot(111)

ax6.plot(len(A2255.axes[0]),0.081,c='mediumpurple',marker='o',lw=0,alpha=0.9)
ax6.annotate(f"Abell 2255",(len(A2255.axes[0])+5,0.081-0.004))
ax6.plot(len(A0023.axes[0]),0.105,c='palegreen',marker='o',lw=0,alpha=0.9)
ax6.annotate(f"Abell 0023",(len(A0023.axes[0])+5,0.105-0.004))
ax6.plot(len(A0267.axes[0]),0.230,c='crimson',marker='o',lw=0,alpha=0.9)
ax6.annotate("Abell 0267",(len(A0267.axes[0])+5,0.230-0.004))
ax6.set_xlim(360,520)
ax6.set_ylim(0.0,0.25)
ax6.set_xlabel('Number of galaxies')
ax6.set_ylabel('Redshift')
plt.tight_layout()
plt.savefig("Data/numbervsredshift.pdf")

fig7 = plt.figure(figsize=(5,3.3))
ax7 = fig7.add_subplot(111)

x =  np.arange(0,1,0.01)
y = np.abs(-1.17*x+0.585)
ax7.plot(x,y,'k--',alpha=0.3)

ax7.plot(a2255/len(A2255.axes[0]),0.081,c='mediumpurple',marker='o',lw=0,alpha=0.9)
ax7.plot((len(A2255.axes[0])-a2255)/len(A2255.axes[0]),0.081,c='mediumpurple',marker='o',lw=0,alpha=0.9)
ax7.annotate(f"A2255 spirals",(a2255/len(A2255.axes[0])+0.03,0.081-0.004))
ax7.annotate(f"A2255 eliptical",(((len(A2255.axes[0])-a2255)/len(A2255.axes[0]))-0.29,0.081-0.004))

ax7.plot(a0023/len(A0023.axes[0]),0.105,c='palegreen',marker='o',lw=0,alpha=0.9)
ax7.plot((len(A0023.axes[0])-a0023)/len(A0023.axes[0]),0.105,c='palegreen',marker='o',lw=0,alpha=0.9)
ax7.annotate(f"A0023 spirals",(a0023/len(A0023.axes[0])-0.28,0.105-0.004))
ax7.annotate(f"A0023 eliptical",(((len(A0023.axes[0])-a0023)/len(A0023.axes[0]))+0.02,0.105-0.004))

ax7.plot(a0267/len(A0267.axes[0]),0.230,c='crimson',marker='o',lw=0,alpha=0.9)
ax7.plot((len(A0267.axes[0])-a0267)/len(A0267.axes[0]),0.230,c='crimson',marker='o',lw=0,alpha=0.9)
ax7.annotate(f"A0267 spirals",(a0267/len(A0267.axes[0])-0.28,0.230-0.004))
ax7.annotate(f"A0267 eliptical",(((len(A0267.axes[0])-a0267)/len(A0267.axes[0]))+0.02,0.230-0.004))

ax7.set_xlim(0,1)
ax7.set_ylim(0.0,0.25)
ax7.set_xlabel('Fraction of galaxies in the cluster')
ax7.set_ylabel('Redshift')
plt.tight_layout()
plt.savefig("Data/fracvsredshift.pdf")
# %%
    