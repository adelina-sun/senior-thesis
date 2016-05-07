<p>Before you test out the application, you'll need the following Python Packages (as some of the files will import them):</p>
<ul><em>Tweepy:</em> https://pypi.python.org/pypi/tweepy/3.5.0</ul>
<ul><em>Geopy:</em> https://pypi.python.org/pypi/geopy</ul>
<ul><em>vincenty:</em> https://pypi.python.org/pypi/vincenty</ul>

<p>In this folder, you'll find:</p>
<ul><b>demo_final.py</b>: The final version of the demo, which assumes that a selection of tweets to be sorted are stored locally (along with their information) in a text file. Make sure the text file containing your tweets is in the same folder on your computer as this one.</ul>
<ul><b>demo_sources.txt</b>: A shorter list of sources (approximately 50). You can use this when calling get_tweets_batch.</ul>
<ul><b>final_sources.txt</b>: The full list of curated sources (130 in total). live_final already calls it, but you can test it out with demo_final as well. Before running anything make sure this file is saved in the same folder as the rest of the Python files (same with demo_sources.txt if you're using it). Otherwise, the application will not be able to find the source information and will crash.</b></ul>
<ul><b>flint.txt</b>: An example batch of tweets that returned when searching for the keyword, "flint." You can test demo_final out on this text file.</ul>
<ul><b>get_tweet_batch.py</b>: Part of the demo, goes hand-in-hand with demo_final.py. Call this first to get tweets and save them locally on your computer. It will ask you to enter a filename for sources. Make sure the text file you want to use is in the same folder!</ul>
<ul><b>live_final.py</b>: The live version of the demo. No need to call any files. It gets tweets straight from Twitter and sorts them.</ul>

<p>Some other notes that might be useful:</p>
<ul>When a file asks for you to enter a filename, there's no need to specify and add ".txt" - just "final_sources" or "demo_sources" is fine.</ul>
<ul>get_tweet_batch (with final_sources) and live_final should not be called more than once every fifteen minutes. You can, it will just crash as it runs up against the Twitter Rate Limit.</ul>
<ul>The weighting works for locality and trendiness when the two variables are given a high priority. It works for recency to an extent. Even when recency is given a high priority, the total weighting still takes into consideration the other two variables. Tweets that come from the same source will have the same trending and distance rank (unless the tweet is considered "breaking"), so if recency is given a high importance, consecutive tweets from the same source will be ranked with the most recent on top (as the recency rank is the only difference in their total weighting). But tweets from other sources might be high in trending/locality rank and might be sorted in between two tweets from the same source (which accounts for the seemingly out-of-order tweets that do not appear in a reverse chronological order). However again, if multiple tweets from the same source are consecutive, the most recent should appear at the top.</ul>
