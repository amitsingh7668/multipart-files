private SingleOutputStreamOperator<EnrichableItemForAttention> 
enrichItemForAttentionForCaseSpecific(SingleOutputStreamOperator<EnrichableItemForAttention> items) {
    boolean hasNullTransformer = items.executeAndCollect()
            .anyMatch(f -> TransformerFactory.getTransformer(f.getItemForAttentionReport().getServiceLine()) == null);

    if (hasNullTransformer) {
        return items;  // Return the input stream without any modification
    }

    return items.filter(f -> TransformerFactory.getTransformer(f.getItemForAttentionReport().getServiceLine()) != null)
                .uid("filter-wrap-as-enrichable-ifa")
                .name("filter-wrap-as-enrichable-ifa")
                .map(m -> TransformerFactory.getTransformer(m.getItemForAttentionReport().getServiceLine()).transform(m))
                .uid("wrap-as-enrichable-ifa")
                .name("wrap-as-enrichable-ifa");
}
