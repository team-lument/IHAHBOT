이미지 폴더는 아래와 같은 구조로 되어 있습니다.

```
📂 image
 ┣ 📂 Background
 ┃ ┗ 📂 Tier
 ┃   ┗ 🖼️ [...TierName].png
 ┃ ┗ 🖼️ BG_Item.png
 ┃ ┗ 🖼️ BG_Right.png
 ┃ ┗ 🖼️ CobaltGame.png
 ┃ ┗ 🖼️ NormalGame.png
 ┃ ┗ 🖼️ RankedGame.png
 ┃ ┗ 🖼️ TeamDuo.png
 ┃ ┗ 🖼️ TeamSolo.png
 ┃ ┗ 🖼️ TeamSquad.png
 ┃ ┗ 🖼️ UnionGame.png
 ┣ 📂 CharacterInfo
 ┃ ┗ 🖼️ [...CharacterName].png
 ┣ 📂 Flags
 ┃ ┗ 🖼️ alpha.png
 ┃ ┗ 🖼️ Clutch.png
 ┃ ┗ 🖼️ omega.png
 ┃ ┗ 🖼️ submarine.png
 ┃ ┗ 🖼️ wickline.png
 ┣ 📂 Items
 ┃ ┗ 🖼️ [...itemCode].png
 ┣ 📂 Rank
 ┃ ┗ 🖼️ [...rank].png
 ┣ 📂 skinFull
 ┃ ┗ 🖼️ [...skinCode].png
 ┣ 📂 TacticalSkills
 ┃ ┗ 🖼️ [...TacticalSkillCode].png
 ┣ 📂 Tier
 ┃ ┣ 📂 Full
 ┃ ┃ ┗ 🖼️ [...TierName].png
 ┃ ┗ 📂 Small
 ┃   ┗ 🖼️ [...TierName].png
 ┣ 📂 Trait
 ┃ ┗ 🖼️ [...TraitCode].png
 ┗ 📂 Weapons
   ┗ 🖼️ [...Weapon].png
```

각 변수명에 대해 설명드리겠습니다.

`TierName`: 티어의 영어 이름을 적습니다. 단, 데미갓은 `Demigod`, 이터니티는 `Eternity`로 표기합니다.<br>
`CharacterName`: 캐릭터의 영어 이름을 적습니다.<br>
`itemCode`: 아이템 코드를 적습니다.<br>
`rank`: `rank1` ~ `rank8`까지 `rank(n)`이 있습니다. 기본 파일로 제공됩니다.<br>
`skinCode`: 해당 스킨의 코드를 적습니다. 이는 DB에서 조회하는 코드로 `characterName_skinNum` 꼴로 이루어져 있습니다. (예를 들어 멧현우라면 `Hyunwoo_5`로 지정해야 합니다)<br>
`TacticalSkillCode`: 30부터 150까지 100을 제외한 10씩 상승하는 값입니다. 차례대로 블링크부터 치유의 바람까지 입니다.<br>
`TraitCode`: 특성 코드를 적습니다. aya.gg 특성 코드와 이터널 리턴 오픈API의 특성 코드가 달라 확인 후 파일을 넣어주세요.<br>
`Weapon`: 각 무기 분류의 영어 이름을 적습니다.
