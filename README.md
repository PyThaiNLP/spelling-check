# Thai_Spell_Check
Thai Spell Check using Conditional Random Field (CRF) (Machine learning)

## Requirements

- PyThaiNLP
- sklearn-crfsuite

## Using

```python
import pythaispell
print(pythaispell.get("สวัสดีนะคับผม"))
```
result 

```
สวัสดีนะ<คำผิด>คับ</คำผิด>ผม
```

The words in <คำผิด> are wrong words.

## License

   Copyright 2019 Wannaphong Phatthiyaphaibun

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
limitations under the License.
