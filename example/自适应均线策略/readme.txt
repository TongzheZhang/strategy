http://school.algostars.com.cn/course/content?id=471 
来自于宁永健这门课 量化交易专题：自适应均线的介绍
指标 Adape Mov，信号 Adapt Mov1。
1. 三连阳或三连阴时才会进场（此时的进场是用
到了K棒形态的概念）；
2. 每次自适应均线变红色或黄色的后续时段内，
只会入场一次，直到由黄变红，或由红变黄；（此语句可以减少进场次数）；
3. 当自适应均线颜色变化之后，立刻对所持有的
部位了结;

value1 是通过短期和长期ATR的比值，来判断市场上价格波动的移动力度，作为突破入场的一个契机

flag = 1 或 0 代表着价格是否在均线上面（状态）

value2 表示当根bar是否有穿的动作

在红黄交叉显示频繁的时候，会频繁入场，此时为了减少交易次数，进行如下限制。value2记录了状态保持的bar数，condition3代表是否大于5。
if condition1 or condition2 then
value2=0;
if flag=1 or flag=0 then
value2=value2+1;
condition3=value2>5;

countif(close>Open,3)=3 判断是否三连阳

