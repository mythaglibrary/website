---
title: How to Build a Team
description: How to build a Morimens team with example comps, including wheels, covenants, and posse recommendations.
icon: lucide/blocks
---

# How to Build a Team

<figure markdown="span">
  ![](/images/emojis/ramona-wise.png){width="128"} <figcaption>"A Keeper needs partners they can count on. Isn't that right, partner?"</figcaption>
</figure>

!!! note "Quick Start Guide"

    1. Pick a character as your **main DPS**.
    2. Add 3 **supports**.
    3. Make sure you have **weakness** and **vulnerable**.
    4. If you finished Faded Legacy Ch. 7, one support should be a **keyflare bot** holding the covenant [Life Drain](#life-drain) and two Keyflare Regen wheels.

## The Purpose of a Team

**How you build a team depends on what you are using it for.**

When you build a team in Morimens, you aren't building it for no reason. Your goal is to use that team to clear a specific stage, in a specific game mode and ruleset.

**The "best" team you can make is different for every stage.** There is no such thing as a team that can do everything. Even if you have a super-strong carry like [Mouchette](/handbook/awakeners/chaos/mouchette) or [GLotan](/handbook/awakeners/primordia-chaos/glotan), they will still get hard countered by some bosses.

Most characters in this game are situationally good — they perform much better in certain situations than others. Part of learning Morimens is understanding which situations are best for each character and which characters are best for each stage.

**The best wheels and covenants depend on the stage too.** For example, in [Faded Legacy](/handbook/storylines#faded-legacy-arc-1) stages, you should be using a lot of [R wheels](/handbook/storylines#r-wheels) unless you have a good reason otherwise.

## How Do You Win?

**Every team starts with a plan on how it is going to win.**

In Morimens, the way you beat stages is by reducing the boss HP to 0 before your own HP runs out. There are different approaches to this you can take.

- You can focus on dealing damage, so all the enemies die before you do.
- You can focus on shielding and healing, so you can take as long as you want to kill enemies.
- You can focus on a specific mechanic, such as poison or counter, and characters that have synergy with that mechanic.

All of these are viable approaches. The important part is to **know what your team is trying to do**. If you don't know your path to victory, if you just use awakeners because they're from the same realm or use wheels because they're auto-recommended by the game, your team might not actually have a way to win.

## Types of Teams

### Hypercarry

```team
name: Caro Mouchette
context: Faded Legacy - Story
summary: A team that enables Mouchette to kill as fast as possible
posse: tiny-wish
members:
  - awakener: mouchette
    archetype: dps
    role: DPS
    note: Main damage dealer
    covenant: crimson-pulse
    wheels: [blade-of-the-titan, analysis-of-death]
  - awakener: ramona
    archetype: support
    role: Support
    note: Keyflare, searches for key cards
    covenant: burial-grounds-sighs
    wheels: [elevated-focus, frenzy]
  - awakener: aigis
    archetype: support
    role: Support
    note: Stuns, applies vulnerable
    covenant: burial-grounds-sighs
    wheels: [gluttony, whisper]
  - awakener: helot
    archetype: support
    role: Support
    note: Buffs Strike damage
    covenant: burial-grounds-sighs
    wheels: [aged, emerge]
```

**The most common type of team, best for new players.**

A hypercarry team is built around a single damage dealer (the "DPS" or "carry") who can potentially deal enough damage to clear the stage by themselves.

The other 3 characters are there to support the DPS. The most important things they can provide are:

- **keyflare** for posses (and [Keyflare Rouse](/handbook/storylines#keyflare-rouse) in [Astral Reign](/handbook/storylines#astral-reign-arc-2))
- the **vulnerable** debuff (+50% damage dealt)
- the **weakness** debuff (-25% damage taken)

The supports can also provide:

- damage buffs for the DPS, like STR and crit buffs
- aliemus, so the team can exalt more often
- arithmetica and cards, so the team can do more stuff every turn
- healing and shielding, for dangerous fights or multi-phase bosses

Sometimes the supports include secondary DPS who also contribute damage. For example, [GMurphy](/handbook/awakeners/benthos-aequor/gmurphy) has trouble killing multiple enemies at once, so you might bring [Tulu](/handbook/awakeners/aequor/tulu), who is both a good support for her and a good damage dealer against mob waves.

The [Newbie DPS Tier List](/handbook/tier-list) and [Newbie Support Tier List](/handbook/tier-list) rank characters based on how well they fit into this type of team.

### Stall

```team
name: Castor Agrippa Stall
context: Astral Reign - D-Effect Zone
summary: A team that outlasts enemies while waiting for relics to kill them
posse: derision-of-destiny
members:
  - awakener: castor
    archetype: tank
    role: Tank
    note: Shields, applies weakness
    covenant: dream-of-medicine
    wheels: [unbearable-freedom, data-is-flesh]
  - awakener: leigh
    archetype: tank
    role: Tank
    note: Heals and shields
    covenant: cursed-rabbit
    wheels: [the-gluttons-tale, noblemans-staff]
  - awakener: agrippa
    archetype: support
    role: Support
    note: Alert, embryos, poison
    covenant: burial-grounds-sighs
    wheels: [pale-descendant, mind-barrier]
  - awakener: erica
    archetype: support
    role: Support
    note: Keyflare, shields, temp. alert
    covenant: life-drain
    wheels: [core-meltdown, moment-of-reunion]
```

**A steady grind for patient players.**

A stall team is based on surviving as long as possible. If you can survive forever, you don't need to do much damage to beat a stage — a bit of damage each turn is enough.

This type of team is most common in D-Effect Zone, where some stages start you with a relic that generates poison or counter. Having an external source of damage means you can focus completely on defense and still win.

Stall teams have to be wary of [Gaze](/handbook/storylines#light-cone-of-fate) if they take too long in normal fights. They also have to actually survive every attack to work properly. Some bosses deal too much damage, or scale too much over time, to be stalled.

### Poison

```team
name: Xu Poison
context: Astral Reign - Story
summary: A team that applies poison and triggers it to deal damage.
posse: plague-of-illusions
members:
  - awakener: xu
    archetype: dps
    role: Poison / DPS
    note: Applies and triggers poison
    covenant: steppenwolf
    wheels: [gift-of-decay, cursed-binding]
  - awakener: nymphaea
    archetype: support
    role: Poison / Support
    note: Keyflare, triggers poison
    covenant: life-drain
    wheels: [merciful-nurturing, moment-of-reunion]
  - awakener: gdoll
    archetype: support
    role: Poison / Support
    note: Aliemus, applies poison
    covenant: dream-of-medicine
    wheels: [manikin-of-oblivion, elevated-focus]
  - awakener: faint
    archetype: tank
    role: Tank
    note: Death resistance, weakness
    covenant: burial-grounds-sighs
    wheels: [dusk-and-dawn, cloaked-in-the-night]
```

**An alternative strategy that ramps up over time.**

Poison characters get stronger the more of them you put together. The more poison you apply, the more damage you deal by triggering poison, and the better overall the team becomes.

**Poison teams are slow unless they actively trigger poison.** This is important in [Astral Reign](/handbook/storylines#astral-reign-arc-2), where there's a maximum amount of poison you can apply.

When building a poison team, consider which characters will apply poison and which characters will trigger poison. Most poison characters can do both, but some are better at applying poison (and should be built as damage dealers), while others are better at triggering poison (and should be built as supports).

A poison team is usually also a stall team, but it can be faster depending on the characters you use. A team with [Liz](/handbook/awakeners/ultra/liz) and [Xu](/handbook/awakeners/caro/xu) can apply tons of poison and trigger it right away, killing as fast as a hypercarry team.

**Poison teams need to rouse everyone in [Astral Reign](/handbook/storylines).** This is because [Prismatic Lens](/handbook/storylines/#prismatic-lens) makes poison tick faster each turn for each roused character in the team.

### Counter

```team
name: Counter Bluwil
context: Faded Legacy - Story Hard Mode
summary: A team that can stack counter and convert it into damage
posse: a-mouses-wisdom
members:
  - awakener: tawil
    archetype: dps
    role: DPS
    note: Keyflare, STR, damage, shields, utility
    covenant: dream-of-medicine
    wheels: [wheel-unseen, blade-of-the-titan]
  - awakener: hameln
    archetype: support
    role: Support
    note: Keyflare, arithmetica, card draw
    covenant: life-drain
    wheels: [merciful-nurturing, frenzy]
  - awakener: caecus
    archetype: support
    role: Counter / Support
    note: Heals, turns STR into counter
    covenant: april-tribute
    wheels: [fin-of-sorrow, to-my-dearest-friend]
  - awakener: nautila
    archetype: tank
    role: Counter / Tank
    note: Shields, turns counter into damage
    covenant: cursed-rabbit
    wheels: [gluttony, emerge]
```

**A niche strategy for specific fights.**

Counter teams are about stacking so much counter that enemies die when they attack you. At low levels, this is pretty easy. At endgame, it's harder, but [Daffodil](/handbook/awakeners/ultra/daffodil) and [Caecus](/handbook/awakeners/aequor/caecus) can do it because their counter scales with buffs.

The effectiveness of counter varies depending on the stage. It's amazing when enemies do a lot of multihit attacks. It's awful against enemies that attack in big single hits, or against attacks that don't trigger counter (such as poison, bleed, or tentacles).

A good counter team has a plan B for when the enemies don't trigger counter. The example team can use [Tawil](/handbook/awakeners/chaos/tawil) as a normal DPS and just kill enemies with Tawil's cards. It can also use [Nautila](/handbook/awakeners/chaos/nautila)'s exalt to convert counter into guaranteed damage.

**If you rely on permanent counter, you need to rouse everyone in [Astral Reign](/handbook/storylines).** This is because [Prismatic Lens](/handbook/storylines/#prismatic-lens) gives you bonus temporary counter each turn for each roused character in the team.

## What Every Team Needs

### The Almighty Keyflare Bot

<figure markdown="span">
  [![Life Drain](/images/covenants/life-drain--icon.png "Life Drain"){width="128" loading=lazy}](#life-drain)
  <span class="flex-center">
    ![Rewinding Time](/images/wheels/rewinding-time.png "Rewinding Time"){width="64" loading=lazy} ![Winter's Requiem](/images/wheels/winters-requiem.png "Winter's Requiem"){width="64" loading=lazy} ![Core Meltdown](/images/wheels/core-meltdown.png "Core Meltdown"){width="64" loading=lazy} ![Moment of Reunion](/images/wheels/moment-of-reunion.png "Moment of Reunion"){width="64" loading=lazy} ![Elevated Focus](/images/wheels/elevated-focus.png "Elevated Focus"){width="64" loading=lazy} ![Gateway of Truth](/images/wheels/gateway-of-truth.png "Gateway of Truth"){width="64" loading=lazy}
  </span> <figcaption>So much power…</figcaption>
</figure>

<span class="inline-flex-center">**Keyflare** ![](/images/icons/stats/keyflare-regen.png#only-dark){width="10" loading=lazy} ![](/images/icons/stats/keyflare-regen--dark.png#only-light){width="10" loading=lazy}</span> **is the best resource in the game.** Your posse is very powerful and having a lot of keyflare lets you use it every turn. Keyflare is even more important in [Astral Reign](/handbook/storylines#astral-reign-arc-2), as you need it to [Keyflare Rouse](/handbook/storylines#keyflare-rouse).

**This is what your keyflare bot is for.** The job of a keyflare bot is to hold the covenant [Life Drain](#life-drain) (unlocked after completing Faded Legacy Chapter 7) and as much Keyflare Regen as possible. This will give you keyflare at the end of each turn and whenever you play their cards.

**You need a keyflare bot.** The moment you unlock [Life Drain](#life-drain), you should be putting it on every team. There are only a few reasons not to do this:

- Your team is Caro, so [Life Drain](#life-drain) has a different effect. You still need a keyflare bot, but you can use a different covenant set if you don't want the embryo.
- Your team is [Primordia: Chaos](#mono-chaos-teams), so the keyflare system is different, and you get a lot of keyflare at the start of the battle.
- You are a speedrunner and planning to finish every battle on turn 1, so [Life Drain](#life-drain)'s end-of-turn effect will never trigger.
- You are playing a [GMurphy](/handbook/awakeners/benthos-aequor/gmurphy) team and your main DPS already makes tons of keyflare.

Dedicated keyflare supports like [Ramona](/handbook/awakeners/chaos/ramona) and [Aigis](/handbook/awakeners/caro/aigis) scale with Keyflare Regen and don't need any other stats to work, making them the best keyflare bots. However, any character can be a keyflare bot as long as they hold [Life Drain](#life-drain) and Keyflare Regen wheels.

<h3 class="flex-center-inline" markdown="span">
  ![](/images/icons/effects/weakness.png){width="24" loading=lazy}
  <span style="color: var(--md-effect-weakness)">Weakness</span>
  &
  ![](/images/icons/effects/vulnerable.png){width="24" loading=lazy}
  <span style="color: var(--md-effect-vulnerable)">Vulnerable</span>
</h3>

<figure markdown="span">
  ![](/images/posses/voices-in-your-head.png){width="128" loading=lazy} <figcaption>The voices are telling you to put weakness and vulnerable on your team.</figcaption>
</figure>

Do you like taking less damage? How about 25% less damage?

Do you like dealing more damage? How about 50% more damage?

**Weakness and vulnerable are the best debuffs in the game.** There's a huge difference between a team that can consistently apply weakness and vulnerable and a team that can't.

Some characters, like [Thais](/handbook/awakeners/caro/thais) and [Horla](/handbook/awakeners/ultra/horla), can achieve close to 100% uptime of weakness and vulnerable. These are naturally the best supports in the game.

Even if you don't have 100% uptime, you should have weakness and vulnerable somewhere, so you have them when you really need them. For example, [Erica](/handbook/awakeners/ultra/erica)'s exalt inflicts vulnerable for one turn, which is good enough to unload all your burst damage.

Teams that don't want weakness or vulnerable are rare:

- [GLotan](/handbook/awakeners/primordia-chaos/glotan) gets stronger when there’s more incoming damage, so inflicting weakness is a DPS loss.
- [Mouchette](/handbook/awakeners/chaos/mouchette) prefers to trigger death resistance rather than mitigate damage, so her teams don't need weakness.
- Fixed poison and counter aren't affected by vulnerable, so characters like [Faros](/handbook/awakeners/aequor/faros) that deal damage mainly through status effects benefit less from it.

**If all else fails, you can run the [Voices In Your Head](https://skeydb.com/database/posses/voices-in-your-head){target="_blank"} posse**, and cry yourself to sleep dreaming of all the other posses you could use if only you had weakness and vulnerable on your team.

## Realms & Teambuilding

<figure markdown="span">
  ![](/images/emojis/miryam-embracing.png){width="128" loading=lazy} <figcaption>"The best realm is clearly Aequor, the Divine Realm of my lord!" <br /> Miryam is not a good source of teambuilding advice.</figcaption>
</figure>

**Choose your characters first and your realm second.**

Characters have the most impact on a team. The "best realm" for your team is the realm of whatever the best character on your account is.

However, realms do have an impact on how a team will play. If you need to choose between 2 equally good supports that are from different realms, the effect of adding the second realm might be the deciding factor.

Here is a quick guide to what each realm means for a team.

### Mono Chaos Teams

![](/images/realms/chaos.png){width="64" loading=lazy}

**Nonstop posses and exalts.**

In Mono Chaos you don't have a gimmick to rely on like any of the other realms. Instead, you get more keyflare and more aliemus. A good Mono Chaos team uses dual posse every turn and abuses the Chaos Realm Mastery effect to exalt every turn.

**Mono Chaos isn't a good option for new players.** It's great if you're a veteran player with 50 unlocked posses, OE characters, and +12 realm mastery wheels. It sucks if your only options from dual posse are [Voices In Your Head](https://skeydb.com/database/posses/voices-in-your-head){target="_blank"} and [Tiny Wish](https://skeydb.com/database/posses/tiny-wish){target="_blank"}.

**Primordia Chaos:** Some characters like [GLotan](/handbook/awakeners/primordia-chaos/glotan) change how Chaos mechanics work when they're on your team. In Primordia Chaos, the normal Chaos mechanics no longer apply; keyflare generation works differently; rouses have Prepare 1 and trigger your equipped posse; and your posse button lets you combine random unlocked posses.

### Teams with Aequor

![](/images/realms/aequor.png){width="64" loading=lazy}

**Consistent shields and bonus damage per hit.**

Aequor gives you a free shield every turn from Tranquil Sea stance, which adds up over long fights. Tentacles also add damage to every hit in Raging Waves stance, which works well with characters that have multihit attacks.

**Tentacle damage scales with Crit Rate and Crit DMG.** Aequor teams can equip more crit wheels and covenants to multiply the effectiveness of their tentacle hits. They can also make good use of teamwide crit buffs, such as the SR wheel [To My Dearest Friend](https://skeydb.com/database/wheels/to-my-dearest-friend){target="_blank"}.

**Passive tentacle damage is good early but weak later on.** When you're fighting level 40+ enemies, you need big damage buffs for your end-of-turn slaps to have any impact. Spamming Tranquil Sea stance for shields is usually better than sitting in Surging Tides stance to get more tentacles.

**Benthos Aequor:** Some characters like [GMurphy](/handbook/awakeners/benthos-aequor/gmurphy) change how Aequor mechanics work when they're on your team. In Benthos Aequor, the stances are stronger but have a 3-turn cooldown.

### Teams with Caro

![](/images/realms/caro.png){width="64" loading=lazy}

**High sustain and aliemus generation.**

You get a lot of free healing by using Crimson Furnace. Embryos let you exalt more often and crit more often. You even get shields and temporary STR when you Devour and trigger the Caro Realm Mastery effect.

**A well-rounded realm for both newbies and veterans.** Adding [Aigis](/handbook/awakeners/caro/aigis) and mixing in Caro is the easiest way for new players to make a good team.

**Remember that you need to build more keyflare.** The [Life Drain](#life-drain) covenant provides embryo fusion instead of keyflare, so your [keyflare bot](#the-almighty-keyflare-bot) will be less effective.

**Propagation Caro:** Some characters like [Saya](/handbook/awakeners/propagation-caro/saya) change how Caro mechanics work when they're on your team. In Propagation Caro, your exalts are buffed; embryos and Realm Mastery further buff your exalts instead of providing shields and STR; and Crimson Furnace is stronger but has a 3-turn cooldown.

### Teams with Ultra

![](/images/realms/ultra.png){width="64" loading=lazy}

**Play more cards, take extra turns.**

Ultra is the strongest support realm. Its realm mechanics are simply the most powerful. Ultra supports like [Clementine](/handbook/awakeners/ultra/clementine) and [Horla](/handbook/awakeners/ultra/horla) are extra valuable because they also give access to Annihilation and Ultra Rounds.

**Pure Ultra depends on how good your characters are.** If you aren't in Aequor or Caro, you don't have free damage, shields, or healing — your cards are all you have. Your characters need to function all by themselves, and you might need a defensive character like [Lily](/handbook/awakeners/chaos/lily) or [Castor](/handbook/awakeners/ultra/castor) to survive long fights.

**Singularity Ultra:** Some characters like [Arachne](/handbook/awakeners/singularity-ultra/arachne) change how Ultra mechanics work when they're on your team. In Singularity Ultra, your command cards are buffed; Ultra Round extends the current turn instead of starting a new turn; and Annihilation is changed to put the leftmost card from Ultra Space into your hand with a 3-turn cooldown.

## Choosing a Posse

<figure class="flex-center" markdown="span">
  ![Tiny Wish](/images/posses/tiny-wish.png "Tiny Wish"){width="64" loading=lazy} ![A Mouse's Wisdom](/images/posses/a-mouses-wisdom.png "A Mouse's Wisdom"){width="64" loading=lazy} ![Warded Injection](/images/posses/warded-injection.png "Warded Injection"){width="64" loading=lazy} ![Obsession Eternal](/images/posses/obsession-eternal.png "Obsession Eternal"){width="64" loading=lazy}
</figure>

**Don't forget the posse is part of the team too.**

Think of the posse as a 5th character on the team. It should round out the team by providing the effect it needs the most. For example:

- If your team needs to exalt to do anything, try [Tiny Wish](https://skeydb.com/database/posses/tiny-wish){target="_blank"}.
- If your team needs a lot of arithmetica to work, try [A Mouse's Wisdom](https://skeydb.com/database/posses/a-mouses-wisdom){target="_blank"}.
- If your team keeps dying and needs more sustain, try [Warded Injection](https://skeydb.com/database/posses/warded-injection){target="_blank"}.
- If your DPS needs STR but your team can't make STR, try [Obsession Eternal](https://skeydb.com/database/posses/obsession-eternal){target="_blank"}.

The [Awakener Guides](/handbook/awakeners) section has a suggested posse for every character, but these are just suggestions. There are many viable posses and you can't repeat posses in D-Effect Zone. Experiment and see what works best for your playstyle.

## Building Characters

<figure markdown="span">
  ![](/images/emojis/aigis-scared.png){width="128" loading=lazy} <figcaption>"Aigis will do her best to be useful!"</figcaption>
</figure>

### Building DPS

DPS builds are straightforward: give them the build that make them deal the most damage.
<h4 class="flex-center-inline" markdown="span">
  ![](/images/icons/stats/crit-rate.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-rate--dark.png#only-light){width="16" loading=lazy}
  ![](/images/icons/stats/crit-dmg.png#only-dark){width="16" loading=lazy}![](/images/icons/stats/crit-dmg--dark.png#only-light){width="16" loading=lazy}
  Crit Rate & Crit DMG
</h4>

[![Mouchette](/images/awakeners/chaos/mouchette--mini.png "Mouchette"){width="80" loading=lazy}](/handbook/awakeners/chaos/mouchette)
[![GMurphy](/images/awakeners/aequor/gmurphy--mini.png "GMurphy"){width="80" loading=lazy}](/handbook/awakeners/aequor/gmurphy)
[![Sorel](/images/awakeners/caro/sorel--mini.png "Sorel"){width="80" loading=lazy}](/handbook/awakeners/caro/sorel)
[![Pollux](/images/awakeners/ultra/pollux--mini.png "pollux"){width="80" loading=lazy}](/handbook/awakeners/ultra/pollux)

**If the DPS can crit, build crit.**

In Morimens, investing in Crit Rate has better returns than Crit DMG, until you have a 100% chance to crit, at which point Crit DMG is obviously better.

When building your DPS, keep in mind which of their skills are actually doing damage. For example, the wheel [Twisted Knight Ballad](https://skeydb.com/database/wheels/twisted-knight-ballad){target="_blank"} increases the Crit Rate and Crit DMG of command cards, but [Sorel](/handbook/awakeners/caro/sorel) benefits very little from it because all her damage comes from her exalt.

**Example SSR wheels:** [Blade of the Titan](https://skeydb.com/database/wheels/blade-of-the-titan){target="_blank"}, [Celestial Beast](https://skeydb.com/database/wheels/celestial-beast){target="_blank"}

**Example SR wheels:** [Analysis of Death](https://skeydb.com/database/wheels/analysis-of-death){target="_blank"}, [Critical Point](https://skeydb.com/database/wheels/critical-point){target="_blank"}

**Example covenants:** [Crimson Pulse](#crimson-pulse), [April Tribute](#april-tribute)

<h4 class="flex-center-inline" markdown="span">
  ![](/images/icons/stats/dmg-amp.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/dmg-amp--dark.png#only-light){width="12" loading=lazy}
  DMG Amplification & Base DMG
</h4>

[![Nymphaea](/images/awakeners/chaos/nymphaea--mini.png "Nymphaea"){width="80" loading=lazy}](/handbook/awakeners/chaos/nymphaea)
[![Faros](/images/awakeners/aequor/faros--mini.png "Faros"){width="80" loading=lazy}](/handbook/awakeners/aequor/faros)
[![Xu](/images/awakeners/caro/xu--mini.png "Xu"){width="80" loading=lazy}](/handbook/awakeners/caro/xu)
[![Arachne](/images/awakeners/ultra/arachne--mini.png "Arachne"){width="80" loading=lazy}](/handbook/awakeners/singularity-ultra/arachne)

**DMG amplification is situational.** It only multiplies Base DMG and effects that create a fixed amount of poison or counter. It doesn't apply to STR or other bonuses to your damage. This means it's only useful for a few types of DPS:

- Those with high Base DMG multipliers, like [GHelot](/handbook/awakeners/caro/ghelot) or [Kathigu-Ra](/handbook/awakeners/chaos/kathigu-ra)
- Those that mainly generate fixed poison or counter, like [Nymphaea](/handbook/awakeners/chaos/nymphaea) or [Faros](/handbook/awakeners/aequor/faros)
- Those that rely on unique effects scaling with DMG amp, like [Castor](/handbook/awakeners/ultra/castor) or [Arachne](/handbook/awakeners/singularity-ultra/arachne)

For DPS that simply have high Base DMG, building crit is usually a higher priority than DMG amp, but they can make good use of incidental DMG amp from relics and substats. They also benefit from effects that boost Base DMG, such as the wheel [Hand of Oblivion](https://skeydb.com/database/wheels/hand-of-oblivion){target="_blank"}.

**DMG amp is teamwide, so it can be on your supports too.** However, DPS that rely on DMG amp often have a talent that gives them bonus scaling from equipped DMG amp gear, so it isn't a waste to put it on them.

**Example SSR wheels:** [Gift of Decay](https://skeydb.com/database/wheels/gift-of-decay){target="_blank"}, [Chains Unbound](https://skeydb.com/database/wheels/chains-unbound){target="_blank"}

**Example SR wheels:** [Cursed Binding](https://skeydb.com/database/wheels/cursed-binding){target="_blank"}, [Sever and Scar](https://skeydb.com/database/wheels/sever-and-scar){target="_blank"}

**Example covenants:** [Steppenwolf](#steppenwolf)

#### Other Considerations

Some characters scale with stats other than crit or DMG amp. For example, [Mouchette](/handbook/awakeners/chaos/mouchette)'s E1 gives her a lot of crit from death resistance. This means building death resistance on Mouchette is as good as building crit on her.

Specific characters may have other needs as well. Some might want the wheel [Will Unyielding](https://skeydb.com/database/wheels/will-unyielding){target="_blank"} to get more strikes and defenses. Others might want the covenant [Dream of Medicine](#dream-of-medicine) to have more copies of a key card.

### Building Supports

[![Ramona](/images/awakeners/chaos/ramona--mini.png "Ramona"){width="80" loading=lazy}](/handbook/awakeners/chaos/ramona)
[![Celeste](/images/awakeners/aequor/celeste--mini.png "Celeste"){width="80" loading=lazy}](/handbook/awakeners/aequor/celeste)
[![Aigis](/images/awakeners/caro/aigis--mini.png "Aigis"){width="80" loading=lazy}](/handbook/awakeners/caro/aigis)
[![Casiah](/images/awakeners/ultra/casiah--mini.png "Casiah"){width="80" loading=lazy}](/handbook/awakeners/ultra/casiah)

Stats don't matter on the vast majority of supports. This means they can hold any wheels and covenants and still do their job.

**In [Faded Legacy](/handbook/storylines#faded-legacy-arc-1), supports should be holding [R wheels](/handbook/storylines#r-wheels)** unless you have a good reason otherwise.

In [Astral Reign](/handbook/storylines#astral-reign-arc-2), they can hold wheels and covenants that give them aliemus, have a useful teamwide effect, or boost the specific supportive thing they do (like healing or shielding).

Some supports do need a specific stat to function. For example, [Faint](/handbook/awakeners/caro/faint)'s exalt is stronger the more death resistance her wheels and covenants have. In this case you should obviously give her as much death resistance as possible.

**Remember to have a [keyflare bot](#the-almighty-keyflare-bot) holding [Life Drain](#life-drain)!**

**Example SSR wheels:** [Dusk and Dawn](https://skeydb.com/database/wheels/dusk-and-dawn){target="_blank"}, [Incalculable Factor](https://skeydb.com/database/wheels/incalculable-factor){target="_blank"}

**Example SR wheels:** [Elevated Focus](https://skeydb.com/database/wheels/elevated-focus){target="_blank"}, [To My Dearest Friend](https://skeydb.com/database/wheels/to-my-dearest-friend){target="_blank"}

**Other wheels:** [R wheels in Faded Legacy](/handbook/storylines#r-wheels)

**Example covenants:** [Burial Ground's Sighs](#burial-grounds-sighs), [Dream of Medicine](#dream-of-medicine), [Deus Ex Machina](#deus-ex-machina)

## Building Covenants

<figure class="flex-center" markdown="span">
  ![Deus Ex Machina](/images/covenants/deus-ex-machina.png "Deus Ex Machina"){width="64" loading=lazy} ![Burial Ground's Sighs](/images/covenants/burial-grounds-sighs.png "Burial Ground's Sighs"){width="64" loading=lazy} ![Life Drain](/images/covenants/life-drain.png "Life Drain"){width="64" loading=lazy}
</figure>

**Binding covenants to your awakeners is not required.** Covenants can be moved freely between teams, and you can repeat covenant sets in D-Effect Zone. This means you only need to build a few sets to use them across all your teams.

You can worry about the minor stat bonus from binding covenants when you’ve played for months and have tons of resources to spend on rerolling extra covenant sets.

**You only need one of each Team Unique set.** If you have two on the same team, the second one does nothing.

### Choosing Stats

Here are the possible main stats for each piece:

| I | II | III | IV | V | VI |
| :-: | :-: | :-: | :-: | :-: | :-: |
| <span class="inline-flex-center">![](/images/icons/stats/crit-rate.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-rate--dark.png#only-light){width="16" loading=lazy} Crit Rate</span> | <span class="inline-flex-center">![](/images/icons/stats/crit-rate.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-rate--dark.png#only-light){width="16" loading=lazy} Crit Rate</span> | <span class="inline-flex-center">![](/images/icons/stats/crit-rate.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-rate--dark.png#only-light){width="16" loading=lazy} Crit Rate</span> | <span class="inline-flex-center">![](/images/icons/stats/aliemus-regen.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/aliemus-regen--dark.png#only-light){width="16" loading=lazy} Aliemus Regen</span> | <span class="inline-flex-center">![](/images/icons/stats/aliemus-regen.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/aliemus-regen--dark.png#only-light){width="16" loading=lazy} Aliemus Regen</span> | <span class="inline-flex-center">![](/images/icons/stats/realm-mastery.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/realm-mastery--dark.png#only-light){width="16" loading=lazy} Realm Mastery</span> |
| <span class="inline-flex-center">![](/images/icons/stats/crit-dmg.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-dmg--dark.png#only-light){width="16" loading=lazy} Crit DMG</span> | <span class="inline-flex-center">![](/images/icons/stats/crit-dmg.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-dmg--dark.png#only-light){width="16" loading=lazy} Crit DMG</span> | <span class="inline-flex-center">![](/images/icons/stats/crit-dmg.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/crit-dmg--dark.png#only-light){width="16" loading=lazy} Crit DMG</span> | <span class="inline-flex-center">![](/images/icons/stats/keyflare-regen.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/keyflare-regen--dark.png#only-light){width="12" loading=lazy} Keyflare Regen</span> | <span class="inline-flex-center">![](/images/icons/stats/keyflare-regen.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/keyflare-regen--dark.png#only-light){width="12" loading=lazy} Keyflare Regen</span> | <span class="inline-flex-center">![](/images/icons/stats/sigil-yield.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/sigil-yield--dark.png#only-light){width="16" loading=lazy} Sigil Yield</span> |
| <span class="inline-flex-center">![](/images/icons/stats/aliemus-regen.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/aliemus-regen--dark.png#only-light){width="16" loading=lazy} Aliemus Regen</span> | <span class="inline-flex-center">![](/images/icons/stats/realm-mastery.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/realm-mastery--dark.png#only-light){width="16" loading=lazy} Realm Mastery</span> | <span class="inline-flex-center">![](/images/icons/stats/dmg-amp.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/dmg-amp--dark.png#only-light){width="12" loading=lazy} DMG Amplification</span> | <span class="inline-flex-center">![](/images/icons/stats/realm-mastery.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/realm-mastery--dark.png#only-light){width="16" loading=lazy} Realm Mastery</span> | <span class="inline-flex-center">![](/images/icons/stats/dmg-amp.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/dmg-amp--dark.png#only-light){width="12" loading=lazy} DMG Amplification</span> | <span class="inline-flex-center">![](/images/icons/stats/dmg-amp.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/dmg-amp--dark.png#only-light){width="12" loading=lazy} DMG Amplification</span> |
| <span class="inline-flex-center">![](/images/icons/stats/keyflare-regen.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/keyflare-regen--dark.png#only-light){width="12" loading=lazy} Keyflare Regen</span> | <span class="inline-flex-center">![](/images/icons/stats/sigil-yield.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/sigil-yield--dark.png#only-light){width="16" loading=lazy} Sigil Yield</span> | <span class="inline-flex-center">![](/images/icons/stats/death-resistance.png#only-dark){width="18" loading=lazy} ![](/images/icons/stats/death-resistance--dark.png#only-light){width="18" loading=lazy} Death Resistance</span> | <span class="inline-flex-center">![](/images/icons/stats/sigil-yield.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/sigil-yield--dark.png#only-light){width="16" loading=lazy} Sigil Yield</span> | <span class="inline-flex-center">![](/images/icons/stats/death-resistance.png#only-dark){width="18" loading=lazy} ![](/images/icons/stats/death-resistance--dark.png#only-light){width="18" loading=lazy} Death Resistance</span> | <span class="inline-flex-center">![](/images/icons/stats/death-resistance.png#only-dark){width="18" loading=lazy} ![](/images/icons/stats/death-resistance--dark.png#only-light){width="18" loading=lazy} Death Resistance</span> |

For most covenant sets, you only care about one or two specific stats and don't care about the rest. On pieces that don't have those stats, you can just pick whatever stat you think will be the least useless.

Personally, I default to <span class="inline-flex-center">![](/images/icons/stats/keyflare-regen.png#only-dark){width="10" loading=lazy} ![](/images/icons/stats/keyflare-regen--dark.png#only-light){width="10" loading=lazy} Keyflare Regen</span> and <span class="inline-flex-center">![](/images/icons/stats/death-resistance.png#only-dark){width="18" loading=lazy} ![](/images/icons/stats/death-resistance--dark.png#only-light){width="18" loading=lazy} Death Resistance</span>, as these stats are always useful regardless of the character, team, or stage.

Some stats to be wary of investing in:

- <span class="inline-flex-center">![](/images/icons/stats/realm-mastery.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/realm-mastery--dark.png#only-light){width="16" loading=lazy} Realm Mastery</span> is only strong in specific realms (Mono Chaos and Benthos Aequor). It's a middling stat for most realm combinations, and nearly useless in base Ultra.
- <span class="inline-flex-center">![](/images/icons/stats/dmg-amp.png#only-dark){width="12" loading=lazy} ![](/images/icons/stats/dmg-amp--dark.png#only-light){width="12" loading=lazy} DMG Amplification</span> is only good for [specific teams](#dmg-amplification-base-dmg).
- <span class="inline-flex-center">![](/images/icons/stats/aliemus-regen.png#only-dark){width="16" loading=lazy} ![](/images/icons/stats/aliemus-regen--dark.png#only-light){width="16" loading=lazy} Aliemus Regen</span> has very low returns on investment and is basically never worth building.

Start by making one of each covenant set you're going to use. When you're a veteran player with a lot of resources, you can build extra covenant sets for specific characters and tailor the stats to exactly what they need.

### Common Meta Covenant Sets

#### Life Drain

<p class="flex-center" markdown="span">
  ![](/images/covenants/life-drain--icon.png){width="136" loading=lazy}
  ![](/images/covenants/life-drain.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 7)*</span>
    <span>**Used by** <br /> Your [keyflare bot](#the-almighty-keyflare-bot)</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Gives keyflare every turn, or embryo fusion in Caro teams.

[As you know](#the-almighty-keyflare-bot), this is the most important covenant set. It's a must-have for any team that wants keyflare (so, every team). In Caro it's less good, but usually still better than other options.

Build as much Keyflare Regen as possible.

#### Burial Ground's Sighs

<p class="flex-center" markdown="span">
  ![](/images/covenants/burial-grounds-sighs--icon.png){width="136" loading=lazy}
  ![](/images/covenants/burial-grounds-sighs.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 4)*</span>
    <span>**Used by** <br /> Any support</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Gives a lot of death resistance, and aliemus when you trigger DR.

This is a good generic covenant set if you don't know what to put on your supports. Death resistance is never bad to have. It isn't Team Unique, so you can put 2 or even 3 sets on your team.

Prioritize Death Resistance and Keyflare Regen.

#### Deus Ex Machina

<p class="flex-center" markdown="span">
  ![](/images/covenants/deus-ex-machina--icon.png){width="136" loading=lazy}
  ![](/images/covenants/deus-ex-machina.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 1)*</span>
    <span>**Used by** <br /> Any support</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

A generic support set that gives a bit of arithmetica.

If you aren't in danger of dying, or if you have a carry like [GHelot](/handbook/awakeners/caro/ghelot) or [GLotan](/handbook/awakeners/primordia-chaos/glotan) who needs a lot of arithmetica, you can run this instead of [Burial Ground's Sighs](#burial-grounds-sighs).

Prioritize Keyflare Regen and any supportive stats of your choice.

#### April Tribute

<p class="flex-center" markdown="span">
  ![](/images/covenants/april-tribute--icon.png){width="136" loading=lazy}
  ![](/images/covenants/april-tribute.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 8)*</span>
    <span>**Used by** <br /> DPS that can crit</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Gives big crit buffs at the start of your turn if the enemies have more than 75% HP remaining.

This is the highest-damage set for most DPS. Most bosses have multiple phases, and each phase counts as a new HP bar, so the condition is easier to fulfil than it looks.

Prioritize Crit DMG, Crit Rate, and Keyflare Regen.

#### Crimson Pulse

<p class="flex-center" markdown="span">
  ![](/images/covenants/crimson-pulse--icon.png){width="136" loading=lazy}
  ![](/images/covenants/crimson-pulse.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Badges)*</span>
    <span>**Used by** <br /> DPS that can crit</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Gives crit rate when you posse. (You have a [keyflare bot](#the-almighty-keyflare-bot), right?)

If you haven't unlocked [April Tribute](#april-tribute), this is the next best option. It's also better in fights where enemies spend most of the fight below 75% HP (such as bosses with death resistance).

Prioritize Crit DMG, Crit Rate, and Keyflare Regen.

#### Dream of Medicine

<p class="flex-center" markdown="span">
  ![](/images/covenants/dream-of-medicine--icon.png){width="136" loading=lazy}
  ![](/images/covenants/dream-of-medicine.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Badges)*</span>
    <span>**Used by** <br /> Characters with key cards to duplicate</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Adds extra copies of the wielder's skill cards to your deck.

This is a powerful covenant set for specific characters where the extra cards make a difference. It's Team Unique, so you have to consider which of your characters needs it the most.

Prioritize crit if a crit DPS is holding this, teamwide stats otherwise. Keyflare Regen is always good.

### Other Covenant Sets

#### Twisted Twins: White

<p class="flex-center" markdown="span">
  ![](/images/covenants/twisted-twins-white--icon.png){width="136" loading=lazy}
  ![](/images/covenants/twisted-twins-white.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 2)*</span>
    <span>**Used by** <br /> Supports with good defense cards</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Gives you a copy of the wielder's defense card every other turn.

This is only worth it if there's something special about the defense that makes you want it every turn. For example, [Horla](/handbook/awakeners/ultra/horla)'s defense inflicts weakness at E1, making this a great covenant set for her.

#### Twisted Twins: Black

<p class="flex-center" markdown="span">
  ![](/images/covenants/twisted-twins-black--icon.png){width="136" loading=lazy}
  ![](/images/covenants/twisted-twins-black.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 3)*</span>
    <span>**Used by** <br /> Supports with good strike cards</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Gives you a copy of the wielder's strike card every other turn.

This is only worth it if there's something special about the strike that makes you want it every turn. For example, [Clementine](/handbook/awakeners/ultra/clementine)'s cards generate STR when played as the first card each turn.

Works great with the SSR wheel [Amidst the Downpour](https://skeydb.com/database/wheels/amidst-the-downpour){target="_blank"}.

#### Unstained Chronicle

<p class="flex-center" markdown="span">
  ![](/images/covenants/unstained-chronicle--icon.png){width="136" loading=lazy}
  ![](/images/covenants/unstained-chronicle.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 5)*</span>
    <span>**Used by** <br /> Supports with high CON</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Heals for a very tiny amount when you use your posse.

Keyflare Regen is a good 3-piece set bonus, but it's hard to imagine a scenario where the healing from this covenant matters.

Maybe if a character with 500 CON is released, this will be good.

#### Returnal Line

<p class="flex-center" markdown="span">
  ![](/images/covenants/returnal-line--icon.png){width="136" loading=lazy}
  ![](/images/covenants/returnal-line.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Verboten Covenant <br /> *(Faded Legacy Ch. 6)*</span>
    <span>**Used by** <br /> Aequor teams with high Realm Mastery</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Gives a tiny amount of STR at the start of the battle; or in Aequor teams, gives a chance to get extra tentacle slaps at end of turn.

Many people misread the effect and think this set generates extra permanent tentacles. In fact, Tentacle Gathering only lasts one turn.

[Vortice](/handbook/awakeners/benthos-aequor/vortice) is the only character that can use this effectively.

#### Steppenwolf

<p class="flex-center" markdown="span">
  ![](/images/covenants/steppenwolf--icon.png){width="136" loading=lazy}
  ![](/images/covenants/steppenwolf.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Rose Scrip)*</span>
    <span>**Used by** <br /> Base DMG and fixed poison/counter DPS</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

For DPS that mainly apply fixed poison or counter, like [Nymphaea](/handbook/awakeners/chaos/nymphaea), this is the highest-damage option.

Prioritize DMG Amplification and Keyflare Regen.

If you can crit, you should probably run [April Tribute](#april-tribute) instead.

#### Organic Form

<p class="flex-center" markdown="span">
  ![](/images/covenants/organic-form--icon.png){width="136" loading=lazy}
  ![](/images/covenants/organic-form.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Rose Scrip)*</span>
    <span>**Used by** <br /> Aliemus supports in [Faded Legacy](/handbook/storylines#faded-legacy-arc-1)</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Increases the wielder's aliemus generation, at the cost of reducing your death resistance.

If you're a god gamer who never dies, you can put this on [Thais](/handbook/awakeners/caro/thais) or [GDoll](/handbook/awakeners/chaos/gdoll) to push your Phantasmal Dive Madness leaderboard score.

Almost useless in [Astral Reign](/handbook/storylines#astral-reign-arc-2) due to rules changes.

#### Scarlet Embrace

<p class="flex-center" markdown="span">
  ![](/images/covenants/scarlet-embrace--icon.png){width="136" loading=lazy}
  ![](/images/covenants/scarlet-embrace.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Sediment)*</span>
    <span>**Used by** <br /> Supports with multihit attacks</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Generates keyflare the first 3 times the wielder hits each turn.

This is a good covenant set, but it only works on supports that attack a lot, and they need to crit to make the most of it. It also costs Sediment, making it an expensive set to build.

Not a good DPS set because it doesn't actually increase damage.

#### Paradox

<p class="flex-center" markdown="span">
  ![](/images/covenants/paradox--icon.png){width="136" loading=lazy}
  ![](/images/covenants/paradox.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Sediment)*</span>
    <span>**Used by** <br /> Tanky DPS that rely on command cards</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Buffs command cards, but makes the wielder's exalt cost more.

For most DPS, this is a lower-damage option than [April Tribute](#april-tribute). Specific characters like [Kathigu-Ra](/handbook/awakeners/chaos/kathigu-ra) and [Salvador](/handbook/awakeners/caro/salvador) can use this because they also benefit from the shielding and healing boost.

#### Photosynthesis Ritual

<p class="flex-center" markdown="span">
  ![](/images/covenants/photosynthesis-ritual--icon.png){width="136" loading=lazy}
  ![](/images/covenants/photosynthesis-ritual.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Badges)*</span>
    <span>**Used by** <br /> Ultra supports in Caro teams</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Makes embryo fusion when the wielder's cards enter Ultra Space.

Not a bad alternative to [Life Drain](#life-drain) in Caro/Ultra teams. Of course, you can just run [Life Drain](#life-drain) instead and not have to build this covenant set.

#### Cocoon of the Maiden

<p class="flex-center" markdown="span">
  ![](/images/covenants/cocoon-of-the-maiden--icon.png){width="136" loading=lazy}
  ![](/images/covenants/cocoon-of-the-maiden.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Badges)*</span>
    <span>**Used by** <br /> Crit DPS in Aequor/Caro teams</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Gives a Crit DMG boost when the wielder Devours or you use an embryo card on them.

Theoretically good in some scenarios, but it takes too much setup for this to be better than [April Tribute](#april-tribute). Not really worth building.

#### Sweet Slug

<p class="flex-center" markdown="span">
  ![](/images/covenants/sweet-slug--icon.png){width="136" loading=lazy}
  ![](/images/covenants/sweet-slug.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Badges)*</span>
    <span>**Used by** <br /> DPS in Aequor/Ultra teams</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Gives a big buff when you switch tentacle stance and use Annihilation in the same turn.

Not a bad effect, but there aren't a lot of Aequor/Ultra teams that can use it effectively. If you have a heavily invested [Vortice](/handbook/awakeners/benthos-aequor/vortice), you can try it out.

#### Feast from Afar

<p class="flex-center" markdown="span">
  ![](/images/covenants/feast-from-afar--icon.png){width="136" loading=lazy}
  ![](/images/covenants/feast-from-afar.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Lightless)*</span>
    <span>**Used by** <br /> Shielders that use their defense a lot</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Boosts the shield from the wielder's defense card. Niche but strong on specific characters like [Kathigu-Ra](/handbook/awakeners/chaos/kathigu-ra).

Usually paired with the SR wheel [The Land of Nonexistence](https://skeydb.com/database/wheels/the-land-of-nonexistence){target="_blank"} or some other way to get more defense cards. Otherwise, this only buffs 1 card in the deck out of 16.

#### Ring of Chamber 36

<p class="flex-center" markdown="span">
  ![](/images/covenants/ring-of-chamber-36--icon.png){width="136" loading=lazy}
  ![](/images/covenants/ring-of-chamber-36.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(Lightless)*</span>
    <span>**Used by** <br /> DPS that rely on their exalt</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Buffs the wielder's exalt, but makes your posse cost more keyflare.

Theoretically better than [April Tribute](#april-tribute) for characters like [Sorel](/handbook/awakeners/caro/sorel), but the drawback is very annoying. It's like the anti-[Life Drain](#life-drain).

Usable if you don't mind having to work harder for your keyflare.

#### Cursed Rabbit

<p class="flex-center" markdown="span">
  ![](/images/covenants/cursed-rabbit--icon.png){width="136" loading=lazy}
  ![](/images/covenants/cursed-rabbit.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(D-Jewels)*</span>
    <span>**Used by** <br /> Shielding and healing supports</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-no)">**Team Unique?** <br /> No</span>
  </span>
</div>

Adds a multiplier to the wielder's shields and healing. A good generic covenant set for defensive characters.

This set is expensive because it costs D-Jewels, which are needed for Dreamshards and other key materials. For most content you can run [Burial Ground's Sighs](#burial-grounds-sighs) and it makes no difference; make sure you actually need this before you start building it.

#### Re-evolution

<p class="flex-center" markdown="span">
  ![](/images/covenants/re-evolution--icon.png){width="136" loading=lazy}
  ![](/images/covenants/re-evolution.png){width="96" loading=lazy}
</p>

<div class="grid cards" markdown>
  <span class="grid-1/1/1">
    <span>**Source** <br /> Store <br /> *(D-Jewels)*</span>
    <span>**Used by** <br /> Supports that exalt in the first fight</span>
    <span style="padding: 0 4px; background-color: var(--md-highlight-yes)">**Team Unique?** <br /> Yes</span>
  </span>
</div>

Essentially a budget [Madness Omen](/handbook/resources#madness-omen), this gives the wielder aliemus in the first fight. It also gives a very tiny amount over time.

This set is expensive because it costs D-Jewels, which are needed for Dreamshards and other key materials. Since it's at best a sidegrade compared to other options, it's hard to recommend.
