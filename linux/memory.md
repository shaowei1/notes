# buffer and cache
共性：
都属于内存，数据都是临时的，一旦关机数据都会丢失。

差异：(先理解前两点，后两点有兴趣可以了解)
A.buffer是要写入数据；cache是已读取数据。
B.buffer数据丢失会影响数据完整性，源数据不受影响；cache数据丢失不会影响数据完整性，但会影响性能。
C.一般来说cache越大，性能越好，超过一定程度，导致命中率太低之后才会越大性能越低。buffer来说，空间越大性能影响不大，够用就行。cache过小，或者没有cache，不影响程序逻辑（高并发cache过小或者丢失导致系统忙死除外）。buffer过小有时候会影响程序逻辑，如导致网络丢包。
D.cache可以做到应用透明，编写应用的可以不用管是否有cache，可以在应用做好之后再上cache。当然开发者显式使用cache也行。buffer需要编写应用的人设计，是程序的一部分。