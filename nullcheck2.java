private SingleOutputStreamOperator<EnrichableItemForAttention> 
enrichItemForAttentionForCaseSpecific(SingleOutputStreamOperator<EnrichableItemForAttention> items) {
    return items.map(m -> {
                Transformer transformer = TransformerFactory.getTransformer(m.getItemForAttentionReport().getServiceLine());
                return transformer != null ? transformer.transform(m) : m;  // Return original item if transformer is null
            })
            .uid("wrap-as-enrichable-ifa")
            .name("wrap-as-enrichable-ifa");
}
