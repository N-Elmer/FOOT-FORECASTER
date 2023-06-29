class FootForecaster {
    constructor() {
      this.yearSlider = $('#year-slider');
      this.yearLabel = $('#year-label');
      this.forecastFig = $('#forecast-fig');
      this.teamWinsFig = $('#team-wins-fig');
      this.topCountriesTable = $('#top-countries-table');
      this.backToTopButton = $('#back-to-top');
  
      this.init();
    }
  
    init() {
      this.attachEventListeners();
      this.updateDashboard(this.yearSlider.val());
      this.checkScrollPosition();
    }
  
    attachEventListeners() {
      this.yearSlider.on('change', () => {
        const year = this.yearSlider.val();
        this.yearLabel.text(year);
        this.updateDashboard(year);
      });
  
      this.backToTopButton.on('click', (event) => {
        event.preventDefault();
        this.scrollToTop();
      });
  
      $(window).on('scroll', () => {
        this.checkScrollPosition();
      });
    }
  
    updateDashboard(year) {
      $.getJSON('/update_dashboard', { year }, (data) => {
        this.updateForecastChart(data.forecast_traces);
        this.updateTeamWinsMap(data.team_wins_trace);
        this.updateTopCountriesTable(data.top_countries_html);
      });
    }
  
    updateForecastChart(traces) {
      const layout = {
        title: 'Forecasted Wins for Each Team',
        font: { color: 'white' },
        xaxis: {
          showgrid: true,
          gridcolor: '#444',
          zerolinecolor: '#444',
          linecolor: '#444',
        },
        yaxis: {
          showgrid: true,
          gridcolor: '#444',
          zerolinecolor: '#444',
          linecolor: '#444',
        },
        paper_bgcolor: '#161C23',
        plot_bgcolor: '#161C23',
      };
      Plotly.newPlot(this.forecastFig[0], traces, layout);
    }
  
    updateTeamWinsMap(trace) {
      const layout = {
        title: 'African Teams and Their Forecasted Wins',
        geo: {
          showframe: false,
          showcoastlines: false,
          projection: { type: 'orthographic' },
          showcountries: true,
          showland: true,
          landcolor: 'rgb(243, 243, 243)',
          showocean: true,
          oceancolor: 'rgb(0, 0, 139)',
        },
        template: 'plotly_dark',
      };
      Plotly.newPlot(this.teamWinsFig[0], [trace], layout);
    }
  
    updateTopCountriesTable(html) {
      this.topCountriesTable.html(html);
    }
  
    checkScrollPosition() {
      const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      if (scrollTop > 20) {
        this.backToTopButton.show();
      } else {
        this.backToTopButton.hide();
      }
    }
  
    scrollToTop() {
      document.body.scrollIntoView({ behavior: 'smooth' });
    }
  }
  
  $(document).ready(() => {
    const footForecaster = new FootForecaster();
  });
  