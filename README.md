# distributed-nose Distribute your tests across multiple nodes with no hassle

## TLDR

### Before

Machine 1:

	$ nosetests long_test_suite
	...
	Ran 1312 tests in 401.109s

Machine 2:

	$ echo "I'm bored :("
	I'm bored :(
	$ uptime | awk -F'load average:' '{ print "Load: " $2 }'
	Load: 0.00, 0.00, 0.00

Developer:

	$ google-chrome http://news.ycombinator.com

### After

Machine 1:

	$ export NOSE_NODES=2;
	$ export NOSE_NODE_NUMBER=1;
	$ nosetests long_test_suite
	...
	Ran 660 tests in 220.502s

Machine 2:

	$ echo "I feel loved"
	I feel loved
	$ export NOSE_NODES=2;
	$ export NOSE_NODE_NUMBER=2;
	$ nosetests long_test_suite
	...
	Ran 652 tests in 214.007s

## The Saga of Your Test Suite

### Oppression of Untested Code

The story of Your Test Suite has its heroes and its villains,
its triumphs and its missteps.
Like many other stories,
it begins with a solitary hero.
Graduating from university,
she joins on with a merry band of software engineering adventurers.
Led by management and supported by a wide cast of characters,
they built things that the common folk loved and needed.

Slowly slowly, things begin to change.
Poorly-structured and strongly-coupled code sneaks in to the code base,
making changes increasingly difficult
and allowing devious bugs to emerge.
Party members begin to regularly break disparate parts of the project,
the realm being too large to survey quickly for one person.
Areas of code become off-limits,
as dragons and unknown things claim all who attempt entry.

Through all this, our hero watches with a heavy heart.
What is to be done about this untested code-base?
Surely she can't change everything by herself?
She is just one person!

Finally, the daily struggles wear her down.

"Enough is enough!"

She resolves, pontificating on how to best strike
against the oppression of untested code.

"I'll write tests, and commit them to source control!"

She says,
understanding that working code is the best possible argument.

### A Nose-fueled Peace

Methodically wielding and teaching [Nose](https://github.com/nose-devs/nose),
she recruits from within to form a merry band of like-minded developers.
They are the fellowship of TDD
and they are determined to succeed.
Tests are committed in flurries of high-value code!

Tales of the fellowship's feats stir excitement in other developers.
Another hero decides that if running some tests is good,
then running all the tests all the time is better!
Brandishing his hat of System Administration,
he utilizes extra server resources and
a Continuous Integration process is born.

Our heroes grow over-confident in their success, however.
Making little attempt to justify the practice,
word of time spent writing tests gets to management.
Managerial Oversight moves to squash our fledgling fellowship.

### Managerial Push-back

"If you have time to write tests,
I must have not given you enough to do!"

They snarl,
threatening with the most dangerous of weapons:
The sling of passive-aggressive disagreement.

Once again, our heroes summon their courage,
and through great effort,
boldly vanquish Managerial Opposition with the sword of high quality.
A new era of peace and productivity begins
and The Project flourishes.

But that peace was not to last.
The specter of Slow Test Runs looms over our heroes.
Soon, test failures go unnoticed.
Developers aren't waiting for tests to finish!
The Test Suite falls in to decay.

### Multiprocess Arrives

Developers grumble and management freely lobs I-Told-You-Sos.
The darkness of the age before tests threatens to return.

"I'll speed up our tests!"

A voice cries out.
It's our hero again,
vowing to strike at the root cause of decay.

Pouring over ancient texts,
she quickly discovers
[Multiprocess](http://nose.readthedocs.org/en/latest/plugins/multiprocess.html).

"This will release us from our single-core shackles."

She proclaims, confident.
Hours later,
her 8-core machine races through tests with alacrity.
Soon, multiprocess is in use on the CI server,
and test speed races forward.

All is right in test land!
Her fellow developers throw a break-room party
in her honor.
Python Meetup talks flow like water
and TDD is once again well-liked by all.

Like the previous peace,
this too is temporary,
as adding more cores is costly.
Fast forward several score tests,
and the once-speedy test suite
regularly brings the beefy, multi-core CI server to its knees.

### Distributed Despair

Remembering the ease of implementing Multiprocess,
our hero knows the drill.
She'll simply distribute the tests across multiple servers!
The same ancient tomes are confidently consulted,
as the solution seemingly obvious.

But wait!

Where are the simple guides?

Our hero isn't a wizard.
She can't decipher the ancient scrolls of distributed systems.
She doesn't have time for formal wizard training,
and the number of moving parts involved is boggling.

Despair sets in as the once-speedy test sweet becomes slower and slower.
The outlook for our adventurers is bleak,
as an evaluation of speeding up the tests themselves reveals immense challenge.
Some even suggest abandoning the test suite entirely
with a new focus on speed!

Factions form and the party threatens to splinter entirely!

### Distributed-Nose: The Scalable Solution

"Wait a minute."

A clear voice breaks through.
It's our hero, once again.

"Why do our test runners need to communicate to coordinate?
Our memcached servers need the same level of coordination
and achieve it with ease!"

Tickled by the flickering of an idea,
she sets to work.
She is steadfast, pouring over tomes on
[Consistent Hashing](http://en.wikipedia.org/wiki/Consistent_hashing).
Once the solution is clear in her mind,
she happens upon a fellow adventurer with sound advice.

"Have you tried distributed-nose?"

"Unfortunately.
I'm terribly allergic to pollen
and I get that every spring."

After the initial confusion is resolved,
it becomes clear to our hero
that other adventurers have already crossed this path.
Hooray!

She quickly skims a strained narrative introduction,
finding it, frankly, quite derivative.
Skipping to the operationalizable section of the tome,
she finds fast success.
This is the tool for them.

With minimal effort,
The Test Suite is distributed across 4 machines.
Test time is slashed and
The Test Suite is saved.
Pondering the future, our hero realizes
she will never again face uncertainty about scalability.
She can always just add more machines!

Test Suite scalability ensured,
our heroes go on to face many other adventures and trials.
But never again would something come so close to erasing their very core
as the oppression of untested code.

## Why distributed-nose?

Scale your tests horizontally across unlimited machines with two test flags.

## Installation

1. Get the project source and install it

    $ pip install distributed-nose

## Usage

To run half your tests on one machine and the other half on the other:

Machine 1:

	$ nosetests --nodes 2 --node-number 1 long_test_suite

Machine 2:

	$ nosetests --nodes 2 --node-number 2 long_test_suite

Alternatively, you can use the environment variables:
* `NOSE_NODES`
* `NOSE_NODE_NUMBER`

### Temporarily disabling test distribution

In the case that you're using environment variables
to control test distribution,
you sometimes still might want to run a one-off test.
Instead of fiddling with environment variables,
you can just use the `--distributed-disabled` flag.

	$ export NOSE_NODES=2;
	$ export NOSE_NODE_NUMBER=1;
	$ nosetests --distributed-disabled long_test_suite

## Distribution algorithm

To determine which node runs which test,
distributed-nose relies on the [hash_ring](https://github.com/Doist/hash_ring)
library's consistent hashing implementation.

By default, tests are individually hashed to the ring.
This results in the most even distribution and the best speed if all tests have the same runtime.
However, it duplicates class setup/teardown work.
If that's expensive, you may want to use `--hash-by-class` or set `NOSE_HASH_BY_CLASS`;
this will hash tests in the same class to the same node.

## Running the test suite

The test suite requires nose, and can be run via `setup.py`:

	# python setup.py nosetests

## Is it Awesome?

Yes. Increasingly so.
