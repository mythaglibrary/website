---
title: Tawil
description: Builds, strategy, and gameplay tips for the Morimens character Tawil.
template: awakeners/awakener.html
awakener:
  tagline: All-in-One Toolbox Engine
  roles:
    - Keyflare
    - Discover
    - Card Draw
    - HP % Damage
    - STR
    - STR Down
    - Multihit
    - Pierce DMG
  ranks:
    dps:
      - tier: B+
        note: Great in Normal Difficulty
    support:
      - tier: A
        note: Game Changing
  stopping_points:
    - 'E2, E3, OE'
  builds:
    - name: Example Build (Keyflare Support)
      covenants:
        - life-drain
      wheels:
        early_game:
          - id: gluttony
            note: (Any support)
          - id: frenzy
            note: (Any support)
        astral_reign:
          - id: merciful-nurturing
            note: (Any Keyflare Regen)
          - id: gateway-of-truth
            note: (Any Keyflare Regen)
    - name: Example Build (Mono Chaos Tank)
      covenants:
        - cursed-rabbit
        - burial-grounds-sighs
      wheels:
        early_game:
          - id: gluttony
            note: (Any support)
          - id: frenzy
            note: (Any support)
        astral_reign:
          - id: memory-spiral
          - id: data-is-flesh
    - name: Example Build (DPS)
      covenants:
        - dream-of-medicine
        - crimson-pulse
      wheels:
        early_game:
          - id: moment-of-reunion
          - id: analysis-of-death
        astral_reign:
          - id: wheel-unseen
          - id: blade-of-the-titan
  suggested_posses:
    - id: a-mouses-wisdom
    - id: festival-of-tides
    - id: all-of-her
      note: In Mono Chaos
  works_well_with:
    - gmurphy
    - lotan
    - gdoll
    - ryker
    - hameln
    - karen
    - celeste
---

Tawil is an extremely complicated and versatile support who has access to every card and ability in the game.

They’re good at generating keyflare, making Them a good [keyflare support](/handbook/team#the-almighty-keyflare-bot). At low levels, They can also deal enough damage to solo DPS.

## Omnifex Convergence

Tawil’s most unique and useful feature is Their exalt. When activated, it discovers 5 random skill cards from other Morimens characters, from which you can choose up to 3 to add to your hand.

The discovered cards come from the realm of Tawil’s current team. For example, if there are Aequor characters in the team, Tawil will only discover cards from Aequor characters. If the team only has Chaos characters, Tawil will discover Chaos cards.

After using Tawil’s exalt, the next Tawil card played will take effect twice. You should take advantage of this to double a particularly impactful card.

At E2, the discovered cards gain Prepare 1, which lets Tawil play the cards discounted or for free. This is obviously a huge buff, so I recommend pulling E2 if you plan to use Tawil.

### Mono Chaos Tawil (Monowil)

At endgame, Tawil is usually used as a support in a [Mono Chaos team](/handbook/team#mono-chaos-teams) (known as **Monowil**).

Chaos lets Tawil discover a lot of shielding and healing cards (e.g. from [Doll](/handbook/awakeners/doll/), [GDoll](/handbook/awakeners/gdoll/), or [Karen](/handbook/awakeners/Karen/)), but unlike the original owners of those cards, Tawil has much better DEF and CON stats, and the Shield and Heal values of those cards are boosted to match. This makes Tawil the best Chaos defensive support in the game.

In addition to being a good tank, Monowil has good access to weakness, and can deal good damage in long fights with [GRamona](/handbook/awakeners/gramona/)’s Predetermined Strike.

Mono Chaos is probably the strongest team for Tawil, but it’s difficult for new players to use, as it relies on having many unlocked posses and high Realm Mastery.

### Aequor Tawil (Bluwil)

For low levels and story stages, Tawil works well in an Aequor team (known as **Bluwil**).

Aequor cards tend to be more synergistic than other realms, as many of them support your tentacles and Tentacle DMG. Aequor also has a lot of generally good cards, like [GMurphy](/handbook/awakeners/gmurphy/)’s Waltz of Lemuria, [Corposant](/handbook/awakeners/corposant/)’s Lightning Retribution, or [Celeste](/handbook/awakeners/celeste/)’s and [Murphy](/handbook/awakeners/murphy/)’s skills that generate arithmetica.

If you want to use Tawil as a DPS, Aequor is a good option, because it boosts Their damage with Raging Waves follow-up hits, and enables Tawil to inflict poison or counter for sustained damage (which Tawil otherwise has problems with).

For new players, Bluwil is the recommended way to play Tawil. It provides decent DPS and good versatility, and it’s easy to play because you can lean on Aequor tentacles for shields or damage.

### Ultra Tawil

Ultra cards are generally not very useful for Tawil, but there are a few interesting things that can be done with Tawil in Ultra teams.

Firstly, Tawil can discover two of [Horla](/handbook/awakeners/horla/)’s Psalms, which means you can have a Horla buff in your team without actually running Horla. The moods Tawil can access are Fear and Happiness, which are unfortunately the weaker ones, but having a permanent buff to your team is still pretty good.

Secondly, Tawil synergizes very well with Ultra Space, and with Ultra supports like [Casiah](/handbook/awakeners/casiah/) and [Arachne](/handbook/awakeners/arachne/). In [Faded Legacy](/handbook/storylines#faded-legacy-arc-1) stages, where there’s no limit on the number of cards you can play, Ultra Tawil can pull off ridiculous turns.

### Caro Tawil

Caro has the fewest cards worth discovering, so Tawil is rarely run in Caro teams. That said, the few cards that are worth discovering ([Thais](/handbook/awakeners/saya/)’s Sacred Blood’s Instinct, [Pickman](/handbook/awakeners/pickman/)’s Chromaphage and Lifelike Rendition, [Saya](/handbook/awakeners/saya/)’s Viscera Blossoms) are very good.

## Pinions & Wings

The other unique feature of Tawil is Their 2-cost skill, **Pinions of Time**.

* **Pinions of Time** puts a card called Twin Wings into your deck when played. At E1, it also gives you an Insight (a 0-cost card that gives 1 arithmetica and draws a card).
* **Twin Wings** deals damage 2 times, generates aliemus for Tawil, puts a card called Four Wings into your deck, and then draws a card. After being played, it’s exhausted.
* **Four Wings** deals damage 4 times, stealing STR with each hit, puts a card called Six Wings into your deck, and then draws a card. After being played, it’s exhausted.
* **Six Wings** deals damage 6 times, in the form of Pierce DMG, and lets you choose from 6 different bonus effects (Memories). Each of these can only be activated once in the exploration. You can also choose not to activate any. After being played, Six Wings is exhausted.

The most important Memory is **Emissary’s Verdict**, which deals damage to the backline enemy equal to 15% of their Max HP. This lets Tawil contribute a significant amount of damage in boss fights, even as a support, on the highest difficulties.

The other Memories are also useful effects, like generating aliemus, searching for cards, or creating a Barrier to block one hit.

If you don’t have enough arithmetica, each Wings card can be played for the cost of 500 Keyflare instead. This is extremely important for DPS Tawil in [Astral Reign](/handbook/storylines#astral-reign-arc-2), where you will often hit [Arithmetica Harmony](/handbook/storylines#arithmetica-harmony) and rely on keyflare-casting for the last few cards.

## The Rest of Tawil’s Kit

**Omniscient Verity**, Tawil’s other skill card, functions as a copy of whatever card is on top of your Draw Pile. This card is mainly a way to generate aliemus for Tawil, but it can be very strong if you get a good card on top.

If you use Omniscient Verity to copy any of Tawil’s Wings, it will be exhausted and removed from your deck, just like the actual Wings are. You might not want to do this if you care about that.

At E3, the first time you hit death resistance in a fight, Tawil gives you **Echoes of the Past**, which rewinds your HP and shield to the previous turn. This is useful in high-difficulty content as effectively an extra HP bar.

## How to Play

Tawil is difficult to play because of all the choices you have to make. When playing with Tawil, keep in mind what role They’re playing on the team, what the end goal of your strategy is, and what choices will be the most effective in reaching that goal.

### Support

If your Tawil isn’t holding DPS gear, or if you’re doing very hard content like ▼ difficulty in D-Effect Zone, it’s safe to say that They won’t be contributing much damage. In this case, you should prioritize Their defensive and supportive utility, which comes from Their discovered cards and the Memories from Six Wings.

When discovering cards, prioritize cards that provide shielding or healing, generate arithmetica or keyflare, or inflict debuffs like weakness and vulnerable. Try to plan ahead and save cards for when they’re needed, so you can get an arithmetica discount from Tawil’s E2. Remember that after using Tawil’s exalt, the next Tawil card played will take effect twice.

Since you only care about Six Wings for the Memories, you only need to play it a maximum of six times in the entire stage, so there’s no need to play Pinions of Time more than necessary.

### DPS

Tawil’s main source of damage is Their Wings, specifically Four Wings. To deal damage with them, you need to set up a turn where you play as many Four Wings as possible.

First, rouse Tawil, then spam Pinions of Time and Twin Wings to stack your deck with many copies of Four Wings. You can also use Tawil’s exalt to discover high-damage cards, such as [GRamona](/handbook/awakeners/gramona/)’s Predetermined Strike or [Corposant](/handbook/awakeners/corposant/)’s Lightning Retribution.

On your burst turn, stack all your damage buffs and then cycle through your deck, playing every Four Wings you see. Because each Four Wings benefits from the temporary STR you’ve already generated, Tawil’s damage scales exponentially with each extra copy you play.

You can finish your combo with Six Wings (which pierces through boss immunity), or with one of Tawil’s discovered cards. If you expect the fight to take a long time, you can end by converting your STR to poison or counter, such as with [Caecus](/handbook/awakeners/caecus/)’s Shattered Halberd, to build up sustained damage.

The double-play effect from Tawil’s exalt can be used to double up Pinions of Time, so you can add more Wings to your deck; or Four Wings, to jump-start your burst damage turn.

In [Astral Reign](/handbook/storylines#astral-reign-arc-2) stages, you’ll probably hit [Arithmetica Harmony](/handbook/storylines#arithmetica-harmony) before the turn ends. To get around this, you can save Tawil’s Wings for last, and play them with keyflare instead of arithmetica.

## Teambuilding

Tawil is usually seen either as a support in a [Mono Chaos team](/handbook/team#mono-chaos-teams), or a carry in an Aequor team.

**Mono Chaos (Monowil):** Tawil is a defensive pillar that can babysit a DPS which otherwise has trouble surviving, such as [Chaos 24](/handbook/awakeners/24/). At endgame, Tawil is often combined with [OE Lotan](/handbook/awakeners/lotan/) and other units that deal Max HP % damage, an effective team against bosses that have only one HP bar.

**Aequor (Bluwil):** One of Tawil’s strongest teammates is [GMurphy](/handbook/awakeners/gmurphy/), who extends Tawil’s combo turns with Abyss Hymns, while also adding a lot of damage. This duo is a top-tier team in any stage without [Arithmetica Harmony](/handbook/storylines#arithmetica-harmony), such as Hectic Skybound Rail and [Faded Legacy](/handbook/storylines#faded-legacy-arc-1) stages like Phantasmal Dive. Tawil also works well with [Celeste](/handbook/awakeners/celeste/), [Caecus](/handbook/awakeners/caecus/), [Murphy](/handbook/awakeners/murphy/), and many other Aequor units.

[Ryker](/handbook/awakeners/ryker/) can search for Tawil’s cards, and boosts Their damage, making Them quite a strong DPS at low levels.

[Hameln](/handbook/awakeners/hameln/) is a very powerful support for Tawil in [Faded Legacy](/handbook/storylines#faded-legacy-arc-1), as he provides the card draw and arithmetica for Tawil to play many more cards in one turn.

For low-budget Tawil teams, [Karen](/handbook/awakeners/karen/), [Ramona](/handbook/awakeners/ramona/), and [GRamona](/handbook/awakeners/gramona/) are also good options.

## High Investment

Tawil’s OE lets you choose from 10 cards instead of 5, significantly improving your odds of getting something good. It also immediately gives 3 arithmetica and grants Tawil a powerful buff so you can set up a combo turn.

## Important Stats

Tawil’s rouse adds a multiplier to Their :skey: Keyflare Regen, making Them a good [keyflare support](/handbook/team#the-almighty-keyflare-bot).

If Tawil is in a [Mono Chaos team](/handbook/team#mono-chaos-teams), They can also hold :realm-mastery: Realm Mastery to boost the Chaos Realm Mastery effect.

Build :crit-dmg: Crit DMG and :crit-rate: Crit Rate if you’re using Tawil as a DPS.