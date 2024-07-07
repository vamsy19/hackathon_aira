import React, { useEffect, useState, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchOrganizations, fetchProjects } from '../services/api/core';
import { Box, Grid, Button } from '@mui/material';
import Leftbar from '../components/workspace/leftbar';
import Rightbar from '../components/workspace/rightbar';
import WorkArea from '../components/workspace/workarea';
import { useNodesState, useEdgesState, addEdge, reconnectEdge } from 'reactflow';

import { createNode, getLayout } from '../services/api/layout';

const WorkspacePage = () => {
    const navigate = useNavigate();
    const [selectedOrganization, setSelectedOrganization] = useState('');
    const [selectedProject, setSelectedProject] = useState('');
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    const onConnect = useCallback(
        (params) => setEdges((eds) => addEdge(params, eds)),
        [setEdges],
    );
    const reconnectDone = useRef(true);

    const onReconnectStart = useCallback(() => {
        reconnectDone.current = false;
    }, []);

    const onReconnect = useCallback((oldEdge, newConnection) => {
        reconnectDone.current = true;
        setEdges((els) => reconnectEdge(oldEdge, newConnection, els));
    }, []);

    const onReconnectEnd = useCallback((_, edge) => {
        if (!reconnectDone.current) {
            setEdges((eds) => eds.filter((e) => e.id !== edge.id));
        }

        reconnectDone.current = true;
    }, []);

    const addSuperNode = async (node) =>{
        const newNodeData = {
            node_type: '1way',
            name: `${node.name}-${nodes.length + 1}`,
            description: node.description,
            project: selectedProject,
            entry_node: node.entry_node,
        }
        
        try {
            const newNode = await createNode(newNodeData);

            const node = {
                id: newNode.id.toString(),
                type: 'oneWay',
                position: { x: 0, y: 0 },
                data: newNode,
            };

            setNodes((nds) => [...nds, node]);
        } catch (error) {
            console.error('Error creating node:', error);
        }


    }

    const addOneWayNode = async () => {
        const newNodeData = {
            node_type: '1way',
            name: `Node ${nodes.length + 1}`,
            description: `Description for node ${nodes.length + 1}`,
            project: selectedProject,
        };

        try {
            const newNode = await createNode(newNodeData);

            const node = {
                id: newNode.id.toString(),
                type: 'oneWay',
                position: { x: 0, y: 0 },
                data: newNode,
            };

            setNodes((nds) => [...nds, node]);
        } catch (error) {
            console.error('Error creating node:', error);
        }
    };

    const addTwoWayNode = async () => {
        const newNodeData = {
            node_type: '2way',
            name: `Node ${nodes.length + 1}`,
            description: `Description for node ${nodes.length + 1}`,
            project: selectedProject,
        };

        try {
            const newNode = await createNode(newNodeData);

            const node = {
                id: newNode.id.toString(),
                type: 'twoWay',
                position: { x: 0, y: 0 },
                data: newNode,
            };

            setNodes((nds) => [...nds, node]);
        } catch (error) {
            console.error('Error creating node:', error);
        }
    };

    const addThreeWayNode = async () => {
        const newNodeData = {
            node_type: '3way',
            name: `Node ${nodes.length + 1}`,
            description: `Description for node ${nodes.length + 1}`,
            project: selectedProject,
        };

        try {
            const newNode = await createNode(newNodeData);

            const node = {
                id: newNode.id.toString(),
                type: 'threeWay',
                position: { x: 0, y: 0 },
                data: newNode,
            };

            setNodes((nds) => [...nds, node]);
        } catch (error) {
            console.error('Error creating node:', error);
        }
    };


    useEffect(() => {
        const checkData = async () => {
            try {
                const organizations = await fetchOrganizations();
                if (organizations.length === 0) {
                    navigate('/create-organization');
                    return;
                }

                const projects = await fetchProjects();
                if (projects.length === 0) {
                    navigate('/create-project');
                    return;
                }
            } catch (error) {
                console.error('Error checking data:', error);
            }
        };

        checkData();
    }, [navigate]);


    useEffect(() => {
        const fetchLayout = async () => {
            if (selectedProject) {
                try {
                    // console.log(selectedProject)
                    const layout = await getLayout(selectedProject);
                    // console.log(layout)
                    var nodes = []
                    var edges = []
                    layout.nodes.forEach((node) => {
                        const { layout_data, ...rest } = node;
                        const new_node = {
                            id: layout_data.id,
                            type: layout_data.type,
                            position: {
                                x: layout_data.position?.x ?? 0,
                                y: layout_data.position?.y ?? 0
                            },
                            data: rest,
                        };
                        nodes.push(new_node);
                    });
                    setNodes(nodes);

                    layout.edges.forEach((edge) => {
                        const new_edge = {
                            id: edge.identifier,
                            source: edge.source.toString(),
                            sourceHandle: edge.source_handle,
                            target: edge.target.toString(),
                            targetHandle: edge.target_handle,
                        }
                        edges.push(new_edge)
                    })
                    setEdges(edges);



                } catch (error) {
                    console.error('Error fetching layout:', error);
                }
            }
        };

        fetchLayout();
    }, [selectedProject]);


    return (
        <Box>
            <Grid container>
                <Grid item xs={2}>
                    <Box sx={{ height: '100%' }}>
                        <Leftbar
                            selectedOrganization={selectedOrganization}
                            setSelectedOrganization={setSelectedOrganization}
                            selectedProject={selectedProject}
                            setSelectedProject={setSelectedProject}
                            addSuperNode={addSuperNode}
                        />
                    </Box>
                </Grid>
                <Grid item xs={7}>
                    <Box sx={{ height: '100%' }}>
                        {selectedProject ? <WorkArea
                            project={selectedProject}
                            nodes={nodes}
                            setNodes={setNodes}
                            onNodesChange={onNodesChange}
                            edges={edges}
                            setEdges={setEdges}
                            onEdgesChange={onEdgesChange}
                            onConnect={onConnect}
                            onReconnect={onReconnect}
                            onReconnectStart={onReconnectStart}
                            onReconnectEnd={onReconnectEnd}
                        /> : null}
                    </Box>
                </Grid>
                <Grid item xs={3}>
                    <Box sx={{ height: '100%' }}>
                        <Rightbar
                            nodes={nodes}
                            setNodes={setNodes}
                            addOneWayNode={addOneWayNode}
                            addTwoWayNode={addTwoWayNode}
                            addThreeWayNode={addThreeWayNode}
                        />
                    </Box>
                </Grid>
            </Grid>
        </Box>
    );
};

export default WorkspacePage;