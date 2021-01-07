{% extends "preview.tpl" %}
{% block content %}
<!-- JUDGES PICS -->
<section class="section-std bg-primary3 font-inverse">
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-6">
				<h3>{{ d.year }} Judges</h3>
				<p>A judging panel of industry experts will be announced in the coming weeks.</p>
				<!-- <p>An eminent judging panel of client- and agency-side experts, chaired by {{ d.chair }}, {{ d.chair_title }}, {{ d.chair_company }} will be reading the entries.</p> -->
			</div>
		</div>
		<div class="tiles-headshots">
			{% for j in d.judges.items() %}
			<a class="tile" href="/{{ WARCAwards }}/{{ d.category }}-judges.info#{{ j.name.replace(' ', '-') }}">
				<img src="/Images/WARCSiteContent/landing-pages/awards/{{ d.cat }}/judges/{{ j.name.replace(' ', '-') }}.jpg" alt="{{ j.name.title() }}">
			</a>
			{% endfor %}	
		</div>
	</div>
</section>
{% endblock %}