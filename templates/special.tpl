{% extends "preview.tpl" %}
{% block content %}
  <section class="section-default bg-background2">
    <div class="container-fluid">
      <h3>Special Awards</h3>
      <div class="tiles-triptych margin-t-medium">
      {% for awd, bio in d.special_awards.items() %}
        <div class="tile-light">
          <h4>{{ awd }}</h4>
          <p>{{ bio }}</p>
        </div>
      {% endfor %}
      </div>
    </div>
  </section>
{% endblock %}