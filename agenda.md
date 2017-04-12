---
layout: blank
---

## Agenda

### Apr 10
Use more computational resources to finish the Tabular Experiment.
The code is available on [https://github.com/jiamings/TabularRLpp](https://github.com/jiamings/TabularRLpp).

#### Azure usage
Currently using 7 instances, D3v2-Promo, D12v2-Promo, D2v2-Promo + 4 F8S.

I find that F8S are cheaper to use since we demand much more CPU than memory.

The jobs that are currently running are [here in this Google doc](https://docs.google.com/document/d/1BziGK-xzp9pLw3hlqdOh4PJQrdHevYJc7J-t9uxej_8/edit?usp=sharing). They should be ready sometime on Wednesday.



### Apr 12

Interestingly, the UBEV-EB results does not seem to be better than MBIE-EB for 100 states under the parameters I select. (Average of 10 runs)

https://github.com/jiamings/TabularRLpp/blob/master/visualization.ipynb

I am trying 0.75 and 0.35 to see if UBEV-EB performance can be improved.