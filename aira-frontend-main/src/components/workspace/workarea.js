import React, { useEffect } from 'react';
import { Box } from '@mui/material';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
} from 'reactflow';

import 'reactflow/dist/style.css';
import oneWayNode from './nodes/oneWayNode';
import twoWayNode from './nodes/twoWayNode';
import threeWayNode from './nodes/threeWayNode';
import { updateLayout } from '../../services/api/layout';

const nodeTypes = {
    oneWay: oneWayNode,
    twoWay: twoWayNode,
    threeWay: threeWayNode,
};

const WorkArea = ({
    project,
    nodes,
    setNodes,
    onNodesChange,
    edges,
    setEdges,
    onEdgesChange,
    onConnect,
    onReconnect,
    onReconnectStart,
    onReconnectEnd,
}) => {



    useEffect(() => {
        console.log('Nodes:', nodes);
        // console.log('Edges:', edges);
        const updateLayoutData = async () => {
            if (nodes.length > 0) {
                try {
                    const layoutData = { project, nodes, edges };
                    await updateLayout(layoutData);
                    // console.log('Layout updated successfully');
                } catch (error) {
                    console.error('Error updating layout:', error);
                }
            }
        };

        updateLayoutData();
    }, [nodes, edges]);
    return (
        <Box sx={{ height: '100vh' }}>
            <div style={{ width: '100%', height: '100%' }}>
                <ReactFlow
                    nodes={nodes}
                    nodeTypes={nodeTypes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    snapToGrid
                    onReconnect={onReconnect}
                    onReconnectStart={onReconnectStart}
                    onReconnectEnd={onReconnectEnd}
                    fitView
                >
                    <Controls />
                    <MiniMap />
                    <Background variant="dots" gap={20} size={1} />
                </ReactFlow>
            </div>
        </Box>
    );
};

export default WorkArea;