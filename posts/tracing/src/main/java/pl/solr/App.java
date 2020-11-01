package pl.solr;

import io.jaegertracing.Configuration;
import io.jaegertracing.internal.JaegerTracer;
import io.jaegertracing.internal.samplers.ConstSampler;
import io.opentracing.Span;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocumentList;
import org.apache.solr.common.params.MapSolrParams;

import java.util.HashMap;
import java.util.Map;

public class App {
    private JaegerTracer tracer;
    private HttpSolrClient solrClient;

    public static void main(String[] args) throws Exception {
        App app = new App();
        app.initTracer();
        app.initSolrClient();
        app.start();
    }

    public void start() throws Exception {
        Span span = tracer.buildSpan("example query").start();

        final Map<String, String> query = new HashMap<>();
        query.put("q", "*:*");
        MapSolrParams queryParams = new MapSolrParams(query);

        final QueryResponse queryResponse = solrClient.query("test", queryParams);
        final SolrDocumentList documents = queryResponse.getResults();

        sleep(10);
        processDocumentsSlow(documents, span, 100);

        span.finish();
    }

    private void processDocumentsSlow(SolrDocumentList documents, Span rootSpan, long sleepTime) {
        Span span = tracer
            .buildSpan("process documents")
            .asChildOf(rootSpan)
            .start();

        processDocumentsSlowNext(documents, span, 300);
        sleep(sleepTime);

        span.finish();
    }

    private void processDocumentsSlowNext(SolrDocumentList documents, Span rootSpan, long sleepTime) {
        Span span = tracer
            .buildSpan("process documents next")
            .asChildOf(rootSpan)
            .start();

        sleep(sleepTime);

        span.finish();
    }

    private void sleep(long millis) {
        try {
            Thread.sleep(millis);
        } catch (Exception ex) {}
    }

    public void initTracer() {
        if (this.tracer == null) {
            Configuration.SamplerConfiguration samplerConfiguration = new Configuration
                .SamplerConfiguration()
                .withType(ConstSampler.TYPE)
                .withParam(1);

            Configuration.ReporterConfiguration reporterConfiguration = Configuration
                .ReporterConfiguration
                .fromEnv();

            Configuration.SenderConfiguration senderConfig = reporterConfiguration
                .getSenderConfiguration()
                .withAgentHost("localhost")
                .withAgentPort(5775);

            reporterConfiguration
                .withLogSpans(true)
                .withSender(senderConfig);

            Configuration configuration = new Configuration("Jaeger with Solr")
                .withSampler(samplerConfiguration)
                .withReporter(reporterConfiguration);

            this.tracer = configuration.getTracer();
        }
    }

    public void initSolrClient() {
        if (this.solrClient == null) {
            this.solrClient = new HttpSolrClient
                .Builder("http://localhost:8983/solr")
                .build();
        }
    }
}
