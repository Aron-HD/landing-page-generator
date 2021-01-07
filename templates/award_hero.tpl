<!-- {% extends "preview.tpl" %} -->
{% block content %}
<section class="section-splash" style="background-image: url(/images/WARCSiteContent/landing-pages/awards/{{ d.award }}/{{ d.image }});">
	<div class="container-wide">
		<div class="splash-inset">
			<h2 class="splash-heading">{{ d.full_award }}</h2>
			<p>{{ d.copy }}</p>
		</div>
	</div>
</section>
<section class="section-default">
	<div class="container-fluid">
		<h2>Categories</h2>
		<div class="tiles-double margin-t-medium">
			{% for x in d.categories %}
			<a class="tile" href="/awards/{{ warc-media-awards / effectiveness }}/{{ x.code }}">
				<h2>{{ x }}</h2>
			</a>
			{% endfor %}
		</div>
	</div>
</section>
{% endblock %}